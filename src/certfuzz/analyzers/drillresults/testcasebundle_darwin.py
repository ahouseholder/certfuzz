'''
Created on Jul 2, 2014

@organization: cert.org
'''
import logging
import re

from certfuzz.drillresults.common import carve
from certfuzz.analyzers.drillresults.testcasebundle_base import TestCaseBundle


logger = logging.getLogger(__name__)

# compile our regular expresssions once
RE_CODE_TYPE = re.compile(r'^Code Type:\s+(\S+)')
RE_MAPPED_FRAME = re.compile(
    r'\s?(0x[0-9a-fA-F]+)\s-\s+(0x[0-9a-fA-F]+)\s+.+\s(/.+)')


class DarwinTestCaseBundle(TestCaseBundle):
    really_exploitable = [
        'EXC_BAD_INSTRUCTION',
    ]

    def _get_classification(self):
        self.classification = carve(self.reporttext, "is_exploitable=", ":")
        logger.debug('Classification: %s', self.classification)

    def _get_shortdesc(self):
        self.shortdesc = carve(self.reporttext, "exception=", ":")
        logger.debug('Short Description: %s', self.shortdesc)

    def _check_64bit(self):
        for line in self.reporttext.splitlines():
            m = re.match(RE_CODE_TYPE, line)
            if m:
                code_type = m.group(1)
                if code_type == 'X86-64':
                    self._64bit_debugger = True
                    logger.debug('Using a 64-bit target')

    def _64bit_addr_fixup(self, faultaddr, instraddr):
        return faultaddr, instraddr

    @property
    def _64bit_target_app(self):
        return TestCaseBundle._64bit_target_app

    def _look_for_loaded_module(self, instraddr, line):
        # convert to an int as hex
        instraddr = int(instraddr, 16)

        for pattern in [RE_MAPPED_FRAME]:
            n = re.search(pattern, line)
            if n:
                begin_address = int(n.group(1), 16)
                end_address = int(n.group(2), 16)
                module_name = n.group(3)
                logger.debug(
                    '%x %x %s %x', begin_address, end_address, module_name, instraddr)
                if begin_address < instraddr < end_address:
                    logger.debug('Matched: %x in %x %x %s', instraddr,
                                 begin_address, end_address, module_name)
                    # as soon as we find this, we're done
                    return module_name

    def get_instr(self, instraddr):
        currentinstr = carve(self.reporttext, "instruction_disassembly=", ":")
        logger.debug('currentinstr: %s' % currentinstr)
        return currentinstr

    def get_return_addr(self):
        # This isn't needed on OSX
        pass

    def fix_return_efa(self, faultaddr):
        '''
        No need for this on Darwin
        '''
        return faultaddr

    def get_instr_addr(self):
        '''
        Find the address for the current (crashing) instruction
        '''
        instraddr = None
        instraddr = carve(self.reporttext, 'instruction_address=', ':')
        logger.debug('carved instruction address: %s' % instraddr)
        return self.format_addr(instraddr)

    def get_fault_addr(self):
        '''
        Find the EFA
        '''
        faultaddr = carve(self.reporttext, 'access_address=', ':')
        logger.debug('carved fault address: %s' % faultaddr)
        return self.format_addr(faultaddr)
