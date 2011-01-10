'''
Created on 12 Dec 2010

@author: Mike Thomas
'''

EMPTY_NOTE = "-"
BAR_TYPES = {"NO_BAR": 0,
             "NORMAL_BAR": 1,
             "REPEAT_START": 2,
             "REPEAT_END":4,
             "SECTION_END":8}
COMBINED_BARLINE_STRING = {(BAR_TYPES["NO_BAR"],
                            BAR_TYPES["NORMAL_BAR"]) : "|",
                           (BAR_TYPES["NO_BAR"],
                            BAR_TYPES["REPEAT_START"] | BAR_TYPES["NORMAL_BAR"]) : "|>",
                           (BAR_TYPES["NORMAL_BAR"],
                            BAR_TYPES["NO_BAR"]) : "|",
                           (BAR_TYPES["REPEAT_END"] | BAR_TYPES["NORMAL_BAR"],
                            BAR_TYPES["NO_BAR"]) : "<|",
                           (BAR_TYPES["REPEAT_END"] | BAR_TYPES["SECTION_END"] | BAR_TYPES["NORMAL_BAR"],
                            BAR_TYPES["NO_BAR"]) : "<|",
                           (BAR_TYPES["SECTION_END"] | BAR_TYPES["NORMAL_BAR"],
                            BAR_TYPES["NO_BAR"]) : "||",
                           (BAR_TYPES["NORMAL_BAR"],
                            BAR_TYPES["NORMAL_BAR"]) : "|",
                           (BAR_TYPES["NORMAL_BAR"],
                            BAR_TYPES["REPEAT_START"] | BAR_TYPES["NORMAL_BAR"]) : ">",
                           (BAR_TYPES["REPEAT_END"] | BAR_TYPES["NORMAL_BAR"],
                            BAR_TYPES["NORMAL_BAR"]) : "<"
                           }

