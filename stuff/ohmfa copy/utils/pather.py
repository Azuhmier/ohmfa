"""pather.py
"""




from pathlib import Path
import json
import sys
import copy
import csv
import yaml




class Pather():
    """_summary_
    """

    read_only = False
    pcwd = None


    def get_path_object(self, path) :
        path_obj = Path(path)
        return path_obj

    def get_pdata(self, path_obj, bp_in=None, clear=False, no_exist="error") :
        pdata = None

        # ----- File Does Exists! -----#
        if path_obj.is_file():
        #- Clear
            if not self.read_only and clear :
                path_obj.unlink()
        #- Load
            else :
                pdata = self.pather_read(path_obj)
        # ----- Boiler_plate -----#
        elif bp_in:
            pdata = copy.deepcopy(bp_in)
        # ----- File Does Not Exists! -----#
        # - Make
        elif not self.read_only and no_exist == "make":
            self.pather_write(path_obj, pdata)
        # - Error
        elif no_exist == "error" :
            sys.exit("ERROR: '" + str(path_obj.absolute()) + "' does not Exist")
        return pdata


    def get_plist(self, path, clear = False, no_exist = "error") :
        dir_obj = Path(path)
        plist = []
        if dir_obj.is_dir():
            # ----- Directory Does Exists! -----#
            # - Clear
            if not self.read_only and clear :
                dir_obj.rmdir()
            # - Load
            else :
                plist = list(dir_obj.iterdir())
        else:
            # ----- Directory Does Not Exists! -----#
            # - Make
            if not self.read_only and no_exist == "make":
                dir_obj.mkdir()
            # - Error
            elif no_exist == 'error' :
                sys.exit("ERROR: '" + str(dir_obj.absolute()) + "' does not Exist")
        return plist


    def get_latest_strtime_dir(self, dir_obj) :
        list_of_files = list(dir_obj.glob("*"))
        latest =  max( [int(Path(x).stem) for x in list_of_files] )
        return str(latest)


    def pather_read(self, path_obj,delim=None) :
        with path_obj.open(mode='r', encoding="utf-8") as infile:
            # Json
            if path_obj.suffix == ".json":
                pdata=json.load(infile)
            # yaml
            elif path_obj.suffix in [".yaml", ".yml"]:
                pdata = yaml.safe_load(infile)
            # csv
            elif path_obj.suffix in [".csv"]:
                csv_reader = csv.reader( infile, delimiter=delim)
                csv_list = [ tuple(row) for row in csv_reader ]
                columns = csv_list.pop(0)
                pdata={}
                for row in csv_list :
                    key = row.pop(0)
                    for idx,item in enumerate(row):
                        pdata[key][columns[idx]] = item
            # text
            elif path_obj.suffix in [".txt", ".text"]:
                pdata = infile
            # undefined
            else: 
                sys.exit("Error: file extension "+str(path_obj.suffix)+" is not supported for pather_read!" )
            return pdata


    def pather_write(self, path_obj, pdata) :
        with path_obj.open(mode='w+', encoding="utf-8") as outfile:
            # json
            if path_obj.suffix == ".json":
                json.dump(pdata,outfile)
            # yaml
            elif path_obj.suffix == ".yml":
                yaml.dump(pdata,outfile)
            # text
            elif path_obj.suffix in [".txt", ".text", ".html", ".csv"]:
                if isinstance(pdata,bytes):
                    path_obj.write_bytes(pdata)
                elif isinstance(pdata,str):
                    path_obj.write_text(pdata, encoding="utf-8")
                else:
                    sys.exit()
            # undefined
            else: 
                sys.exit("Error: file extension "+str(path_obj.suffix)+" is not supported for pather_write!" )




class SinglePather(Pather):
    """_summary_

    Args:
        Pather (_type_): _description_
    """

    pdata      = None
    ppath      = None
    plist      = None

    def __init__(self,pdir=None,pname=None,pstem=None,pext=None,read_only=False,bp=None,ptype=None):
        self.pdir = pdir
        self.pname = pname
        self.pstem = pstem
        self.pext = pext
        self.read_only = read_only
        self.ptype = ptype
        self.bp = bp
        if self.pname :
            self.pext = self.pname.suffix
            self.pstem = self.pname.stem


    def gen_ppath(self, clear = False, no_exists = "error"):
        """_summary_
        """
        path_seg = self.pstem+self.pext
        self.ppath = self.pdir.joinpath(path_seg)
        if self.ptype == 'file':
            self.pdata = self.get_pdata(self.ppath,clear=clear,no_exist=no_exists,bp_in=self.bp)
        elif self.ptype == 'dir':
            self.plist = self.get_plist(self.ppath,clear=clear,no_exist=no_exists)


    def write_pdata(self):
        """_summary_
        """
        self.gen_ppath()
        self.pather_write(self.ppath, self.pdata)


    def read_pdata(self):
        """_summary_
        """
        self.gen_ppath()
        self.pdata = self.pather_read(self.ppath)
