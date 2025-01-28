
# PROJECT SETTINGS ::
import os
import sys
import subprocess
import consolemenu as co


if('C:\\matheus\\change_automations_18.0\\' not in sys.path):
    sys.path.append('C:\\matheus\\change_automations_18.0\\')
else: print("❕ Python Path has already loaded to use.")

#\\.. Centralizer's entities ::
from DataCentralizer import DataPayment as Payment
from DataCentralizer import LocalStorage as Storage
from DataCentralizer import CashierDataPaymnt as Cashier
from DataCentralizer import DataCentralizer as Centralizer
from output.FilesHandling import ExternalFilesHandling as ExternalFile
