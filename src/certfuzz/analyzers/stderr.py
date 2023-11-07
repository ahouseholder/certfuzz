'''
Created on Oct 25, 2010

Provides a wrapper around gdb.

@organization: cert.org
'''
import logging
from certfuzz.analyzers.analyzer_base import Analyzer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

OUTFILE_EXT = "stderr"

get_file = lambda x: '%s.%s' % (x, OUTFILE_EXT)


class StdErr(Analyzer):
    def __init__(self, cfg, testcase):
        outfile = get_file(testcase.fuzzedfile.path)
        timeout = cfg['runner']['runtimeout']

        Analyzer.__init__(self, cfg, testcase, outfile, timeout, stderr=outfile)
        # need to set the stderr_redirect flag on the base class
        self.empty_output_ok = True

    def _get_cmdline(self):
        return self.cmdargs
