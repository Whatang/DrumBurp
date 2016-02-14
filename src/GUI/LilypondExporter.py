# Copyright 2016 Michael Thomas
#
# See www.whatang.org for more information.
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DrumBurp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DrumBurp.  If not, see <http://www.gnu.org/licenses/>
'''
Created on Feb 28, 2015

@author: mike_000
'''
from PyQt4.Qt import QThread
import subprocess
import os
import platform

class LilypondExporter(QThread):
    NOT_STARTED = 0
    STARTED = 1
    WROTE_LY = 2
    SUCCESS = 3
    ERROR_IN_WRITING_LY = -1
    ERROR_IN_RUNNING_LY = -2

    def __init__(self, lilypondString, outputPath, lilypondPath, lilyFormat, onFinish = None, parent = None):
        super(LilypondExporter, self).__init__(parent = parent)
        self.lilyString = lilypondString
        self._outputPath = outputPath
        self._processedPath = self._calcProcessedPath(self._outputPath)
        self._onFinish = onFinish
        self._lilypondPath = unicode(lilypondPath)
        self._format = self._toFormatString(lilyFormat)
        self._status = self.NOT_STARTED
        self.returnCode = 0

    def get_status(self):
        return self._status

    @staticmethod
    def _calcProcessedPath(inputPath):
        if inputPath.endswith('.ly'):
            inputPath = inputPath[:-3]
        return inputPath

    @staticmethod
    def _toFormatString(lilyFormat):
        if isinstance(lilyFormat, int):
            if lilyFormat < 0 or lilyFormat > 2:
                lilyFormat = 0
            lilyFormat = ["pdf", "ps", "png"][lilyFormat]
        return unicode(lilyFormat)

    def run(self):
        try:
            self._status = self.STARTED
            with open(self._outputPath, 'w') as handle:
                try:
                    handle.write(self.lilyString.encode('utf-8'))
                except:
                    self._status = self.ERROR_IN_WRITING_LY
                    raise
            self._status = self.WROTE_LY
            if self._lilypondPath is not None:
                kwargs = {}
                if platform.system() == "Windows":
                    suInfo = subprocess.STARTUPINFO()
                    suInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    suInfo.wShowWindow = subprocess.SW_HIDE
                    kwargs['startupinfo'] = suInfo
                env = os.environ
                env['LILYPOND_GC_YIELD'] = '100'
                kwargs['env'] = env
                returnCode = subprocess.call([self._lilypondPath,
                                              '-s',
                                              '-o', self._processedPath,
                                              '-f', self._format,
                                              self._outputPath],
                                             **kwargs)
                self.returnCode = returnCode
                if returnCode == 0:
                    self._status = self.SUCCESS
                else:
                    self._status = self.ERROR_IN_RUNNING_LY

        finally:
            if self._onFinish is not None:
                self._onFinish()
