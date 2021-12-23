import os
import shutil
import tempfile
import logging
import subprocess
import re
import pytest
from glob import glob
from pty import openpty

COVERAGE_SCRIPT = 'python3-coverage'
KICAD_PCB_EXT = '.kicad_pcb'
KICAD_SCH_EXT = '.sch'
REF_DIR = 'tests/reference'
BOARDS_DIR = 'boards'
CONFIGS_DIR = 'configs'

MODE_SCH = 1
MODE_PCB = 0


class TestContext(object):

    def __init__(self, test_dir, test_name, board_name, config_name, sub_dir):
        # We are using PCBs
        self.mode = MODE_PCB
        # The name used for the test output dirs and other logging
        self.test_name = test_name
        # The name of the PCB board file
        self.board_name = board_name
        # The actual board file that will be loaded
        self._get_board_file()
        # The config file we'll use
        self._get_config_name(config_name)
        # The actual output dir for this run
        self._set_up_output_dir(test_dir)
        # Where are we expecting to get the outputs (inside test_name)
        self.sub_dir = sub_dir
        # stdout and stderr from the run
        self.out = None
        self.err = None
        self.proc = None

    def get_board_dir(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(this_dir, '../'+BOARDS_DIR)

    def _get_board_file(self):
        self.board_file = os.path.abspath(os.path.join(self.get_board_dir(),
                                          self.board_name +
                                          (KICAD_PCB_EXT if self.mode == MODE_PCB else KICAD_SCH_EXT)))
        logging.info('KiCad file: '+self.board_file)
        assert os.path.isfile(self.board_file)

    def _get_config_dir(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(this_dir, '../'+CONFIGS_DIR)

    def _get_config_name(self, name):
        if name:
            self.config_file = os.path.abspath(os.path.join(self._get_config_dir(), name+'.ibom.config'))
            logging.info('config file: '+self.config_file)
            assert os.path.isfile(self.config_file)
        else:
            self.config_file = None
            logging.info('No config file')

    def _set_up_output_dir(self, test_dir):
        if test_dir:
            self.output_dir = os.path.join(test_dir, self.test_name)
            os.makedirs(self.output_dir, exist_ok=True)
            self._del_dir_after = False
        else:
            # create a tmp dir
            self.output_dir = tempfile.mkdtemp(prefix='tmp-kiplot-'+self.test_name+'-')
            self._del_dir_after = True
        logging.info('Output dir: '+self.output_dir)

    def clean_up(self):
        logging.debug('Clean-up')
        if self._del_dir_after:
            logging.debug('Removing dir')
            shutil.rmtree(self.output_dir)
        # We don't have a project, and we don't want one
        pro = os.path.join(self.get_board_dir(), self.board_name+'.pro')
        if os.path.isfile(pro):
            os.remove(pro)
        # We don't have a footprint cache, and we don't want one
        fp_cache = os.path.join(self.get_board_dir(), 'fp-info-cache')
        if os.path.isfile(fp_cache):
            os.remove(fp_cache)

    def get_out_path(self, filename):
        return os.path.join(self.output_dir, filename)

    def get_gerber_job_filename(self):
        return os.path.join(self.sub_dir, self.board_name+'-job.gbrjob')

    def get_gerber_filename(self, layer_slug, ext='.gbr'):
        return os.path.join(self.sub_dir, self.board_name+'-'+layer_slug+ext)

    def get_pos_top_filename(self):
        return os.path.join(self.sub_dir, self.board_name+'-top.pos')

    def get_pos_bot_filename(self):
        return os.path.join(self.sub_dir, self.board_name+'-bottom.pos')

    def get_pos_both_filename(self):
        return os.path.join(self.sub_dir, self.board_name+'-both.pos')

    def get_pos_top_csv_filename(self):
        return os.path.join(self.sub_dir, self.board_name+'-top-pos.csv')

    def get_pos_bot_csv_filename(self):
        return os.path.join(self.sub_dir, self.board_name+'-bottom-pos.csv')

    def get_pos_both_csv_filename(self):
        return os.path.join(self.sub_dir, self.board_name+'-both-pos.csv')

    def get_pth_drl_filename(self):
        return os.path.join(self.sub_dir, self.board_name+'-PTH.drl')

    def get_pth_gbr_drl_filename(self):
        return os.path.join(self.sub_dir, self.board_name+'-PTH-drl.gbr')

    def get_pth_pdf_drl_filename(self):
        return os.path.join(self.sub_dir, self.board_name+'-PTH-drl_map.pdf')

    def get_npth_drl_filename(self):
        return os.path.join(self.sub_dir, self.board_name+'-NPTH.drl')

    def get_npth_gbr_drl_filename(self):
        return os.path.join(self.sub_dir, self.board_name+'-NPTH-drl.gbr')

    def get_npth_pdf_drl_filename(self):
        return os.path.join(self.sub_dir, self.board_name+'-NPTH-drl_map.pdf')

    def expect_out_file(self, filename):
        file = self.get_out_path(filename)
        assert os.path.isfile(file)
        assert os.path.getsize(file) > 0
        logging.debug(filename+' OK')
        return file

    def dont_expect_out_file(self, filename):
        file = self.get_out_path(filename)
        assert not os.path.isfile(file)

    def create_dummy_out_file(self, filename):
        file = self.get_out_path(filename)
        with open(file, 'w') as f:
            f.write('Dummy file\n')

    def run(self, ret_val=None, extra=None, use_a_tty=False, filename=None, no_out_dir=False, no_board_file=False,
            no_config_file=False, chdir_out=False, no_verbose=False):
        logging.debug('Running '+self.test_name)
        # We aren't using the dialog
        os.environ['INTERACTIVE_HTML_BOM_NO_DISPLAY'] = ''
        # Change the command to be local and add the board and output arguments
        cmd = [COVERAGE_SCRIPT, 'run', '-a']
        if chdir_out:
            cmd.append('--rcfile=../../.coveragerc')
            os.environ['COVERAGE_FILE'] = os.path.join(os.getcwd(), '.coverage')
        cmd.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))+'/../../InteractiveHtmlBom/generate_interactive_bom.py'))
        cmd.append('--no-browser')
        if not no_out_dir:
            cmd = cmd+['--dest-dir', os.path.abspath(self.output_dir)]
        if extra is not None:
            cmd = cmd+extra
        if not no_board_file:
            cmd.append(filename if filename else self.board_file)
        logging.debug(cmd)
        out_filename = self.get_out_path('output.txt')
        err_filename = self.get_out_path('error.txt')
        if use_a_tty:
            # This is used to test the coloured logs, we need stderr to be a TTY
            master, slave = openpty()
            f_err = slave
            f_out = slave
        else:
            # Redirect stdout and stderr to files
            f_out = os.open(out_filename, os.O_RDWR | os.O_CREAT)
            f_err = os.open(err_filename, os.O_RDWR | os.O_CREAT)
        # Run the process
        if chdir_out:
            cwd = os.getcwd()
            os.chdir(self.output_dir)
        process = subprocess.Popen(cmd, stdout=f_out, stderr=f_err)
        if chdir_out:
            os.chdir(cwd)
            del os.environ['COVERAGE_FILE']
        ret_code = process.wait()
        logging.debug('ret_code '+str(ret_code))
        if use_a_tty:
            self.err = os.read(master, 10000)
            self.err = self.err.decode()
            self.out = self.err
        exp_ret = 0 if ret_val is None else ret_val
        assert ret_code == exp_ret
        if use_a_tty:
            os.close(master)
            os.close(slave)
            with open(out_filename, 'w') as f:
                f.write(self.out)
            with open(err_filename, 'w') as f:
                f.write(self.out)
        else:
            # Read stdout
            os.lseek(f_out, 0, os.SEEK_SET)
            self.out = os.read(f_out, 10000)
            os.close(f_out)
            self.out = self.out.decode()
            # Read stderr
            os.lseek(f_err, 0, os.SEEK_SET)
            self.err = os.read(f_err, 10000)
            os.close(f_err)
            self.err = self.err.decode()

    def search_out(self, text):
        m = re.search(text, self.out, re.MULTILINE)
        return m

    def search_err(self, text):
        m = re.search(text, self.err, re.MULTILINE)
        return m

    def search_in_file(self, file, texts):
        logging.debug('Searching in "'+file+'" output')
        with open(self.get_out_path(file)) as f:
            txt = f.read()
        res = []
        for t in texts:
            logging.debug('- r"'+t+'"')
            m = re.search(t, txt, re.MULTILINE)
            assert m
            # logging.debug(' '+m.group(0))
            res.append(m.groups())
        return res

    def search_not_in_file(self, file, texts):
        logging.debug('Searching not in "'+file+'" output')
        with open(self.get_out_path(file)) as f:
            txt = f.read()
        for t in texts:
            logging.debug('- r"'+t+'"')
            m = re.search(t, txt, re.MULTILINE)
            assert m is None

    def compare_image(self, image, reference=None, diff='diff.png'):
        """ For images and single page PDFs """
        if reference is None:
            reference = image
        cmd = ['compare', '-metric', 'MSE',
               self.get_out_path(image),
               os.path.join(REF_DIR, reference),
               self.get_out_path(diff)]
        logging.debug('Comparing images with: '+str(cmd))
        res = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        m = re.match(r'([\d\.]+) \(([\d\.]+)\)', res.decode())
        assert m
        logging.debug('MSE={} ({})'.format(m.group(1), m.group(2)))
        assert float(m.group(2)) == 0.0

    def compare_pdf(self, gen, reference=None, diff='diff-{}.png'):
        """ For multi-page PDFs """
        if reference is None:
            reference = gen
        logging.debug('Comparing PDFs: '+gen+' vs '+reference)
        # Split the reference
        logging.debug('Splitting '+reference)
        cmd = ['convert', '-density', '150',
               os.path.join(REF_DIR, reference),
               self.get_out_path('ref-%d.png')]
        subprocess.check_call(cmd)
        # Split the generated
        logging.debug('Splitting '+gen)
        cmd = ['convert', '-density', '150',
               self.get_out_path(gen),
               self.get_out_path('gen-%d.png')]
        subprocess.check_call(cmd)
        # Chek number of pages
        ref_pages = glob(self.get_out_path('ref-*.png'))
        gen_pages = glob(self.get_out_path('gen-*.png'))
        logging.debug('Pages {} vs {}'.format(len(gen_pages), len(ref_pages)))
        assert len(ref_pages) == len(gen_pages)
        # Compare each page
        for page in range(len(ref_pages)):
            cmd = ['compare', '-metric', 'MSE',
                   self.get_out_path('ref-'+str(page)+'.png'),
                   self.get_out_path('gen-'+str(page)+'.png'),
                   self.get_out_path(diff.format(page))]
            logging.debug('Comparing images with: '+str(cmd))
            res = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            m = re.match(r'([\d\.]+) \(([\d\.]+)\)', res.decode())
            assert m
            logging.debug('MSE={} ({})'.format(m.group(1), m.group(2)))
            assert float(m.group(2)) == 0.0

    def compare_txt(self, text, reference=None, diff='diff.txt'):
        if reference is None:
            reference = text
        cmd = ['/bin/sh', '-c', 'diff -ub '+os.path.join(REF_DIR, reference)+' ' +
               self.get_out_path(text)+' > '+self.get_out_path(diff)]
        logging.debug('Comparing texts with: '+str(cmd))
        res = subprocess.call(cmd)
        assert res == 0

    def filter_txt(self, file, pattern, repl):
        fname = self.get_out_path(file)
        with open(fname) as f:
            txt = f.read()
        with open(fname, 'w') as f:
            f.write(re.sub(pattern, repl, txt))

    def expect_gerber_flash_at(self, file, res, pos):
        """
        Check for a gerber flash at a given point
        (it's hard to check that aperture is right without a real gerber parser
        """
        if res == 6:  # 4.6
            mult = 1000000
        else:  # 4.5
            mult = 100000
        repat = r'^X{x}Y{y}D03\*$'.format(x=int(pos[0]*mult), y=int(pos[1]*mult))
        self.search_in_file(file, [repat])
        logging.debug("Gerber flash found: "+repat)

    def expect_gerber_has_apertures(self, file, ap_list):
        ap_matches = []
        for ap in ap_list:
            # find the circular aperture for the outline
            ap_matches.append(r'%AD(.*)'+ap+r'\*%')
        grps = self.search_in_file(file, ap_matches)
        aps = []
        for grp in grps:
            ap_no = grp[0]
            assert ap_no is not None
            # apertures from D10 to D999
            assert len(ap_no) in [2, 3]
            aps.append(ap_no)
        logging.debug("Found apertures {}".format(aps))
        return aps


class TestContextSCH(TestContext):

    def __init__(self, test_name, board_name, config_name, sub_dir):
        super().__init__(test_name, board_name, config_name, sub_dir)
        self.mode = MODE_SCH
        self._get_board_file()
