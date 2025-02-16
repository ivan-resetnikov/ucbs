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

import shutil
import os

EXECUTABLE_PATH: str = "./build/bin/main.exe"
INTERMIDIATES_DIR: str = "./build/obj"

shutil.rmtree(INTERMIDIATES_DIR)
os.makedirs(INTERMIDIATES_DIR)
os.remove(EXECUTABLE_PATH)