# Closed-source Code License (CSCL)
# 
# Copyright (C) Ivan Reshetnikov - All Rights Reserved.
# 
# UNAUTHORIZED COPYING OF THIS SOFTWARE OR ITS SOURCE CODE, VIA ANY MEDIUM IS STRICTLY PROHIBITED.
# THE CONTENTS INSIDE THIS PROJECT ARE PROPRIETARY AND CONFIDENTIAL.
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# Written by Ivan Reshetnikov legal@ivan-reshetnikov.dev, February 2025.

import os
import inspect

from ansi import *

def log_debug(message: str) -> None:
    frame = inspect.currentframe().f_back
    line_number = frame.f_lineno
    file_name = os.path.basename(__file__)  # Extract file name without path
    print(f"{FG_WHITE}debug{RESET}:    {FG_WHITE_FAINT}{file_name}:{line_number:<3}{RESET} - {message}")

def log_info(message: str) -> None:
    frame = inspect.currentframe().f_back
    line_number = frame.f_lineno
    file_name = os.path.basename(__file__)  # Extract file name without path
    print(f"{FG_BLUE}info{RESET}:     {FG_WHITE_FAINT}{file_name}:{line_number:<3}{RESET} - {message}")

def log_warning(message: str) -> None:
    frame = inspect.currentframe().f_back
    line_number = frame.f_lineno
    file_name = os.path.basename(__file__)  # Extract file name without path
    print(f"{FG_YELLOW}warning{RESET}:  {FG_WHITE_FAINT}{file_name}:{line_number:<3}{RESET} - {message}")

def log_error(message: str) -> None:
    frame = inspect.currentframe().f_back
    line_number = frame.f_lineno
    file_name = os.path.basename(__file__)  # Extract file name without path
    print(f"{FG_RED}error{RESET}:    {FG_WHITE_FAINT}{file_name}:{line_number:<3}{RESET} - {message}")

def log_critical(message: str) -> None:
    frame = inspect.currentframe().f_back
    line_number = frame.f_lineno
    file_name = os.path.basename(__file__)  # Extract file name without path
    print(f"{BG_RED}critical{RESET}: {FG_WHITE_FAINT}{file_name}:{line_number:<3}{RESET} - {message}")
