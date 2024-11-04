"""pather.py
"""




import os
from pathlib import Path
import json
import sys
import copy
import csv
import yaml




class Pather():
    """_summary_
    """

    


    def __init__(self):
        pass


    def dir_walk(self, path):
        for root, dirs, files in os.walk(path):
            path = root.split(os.sep)
            print((len(path) - 1) * '---', os.path.basename(root))
            for file in files:
                print(len(path) * '---', file)


    def get_file_obj(self, path, bp_in=None, clear=False, no_exist="error") :
        p = Path(path)
        data = None

        if p.is_file():

            # ----- File Does Exists! -----#
            #- Clear
            if not self.dry_run and clear :
                p.unlink()

            #- Load
            else :
                data = self.read(p)

        elif bp_in:
            data = copy.deepcopy(bp_in)

        # ----- File Does Not Exists! -----#
        # - Make
        elif not self.dry_run and no_exist == "make":
            self.write(p,data)

        # - Error
        elif no_exist == "error" :
            sys.exit("ERROR: '" + str(p.absolute()) + "' does not Exist")

        return p, data


    def get_dir_obj(self, path, clear = False, no_exist = "error") :
        """_summary_

        Args:
            path (_type_): _description_
            clear (bool, optional): _description_. Defaults to False.
            no_exist (str, optional): _description_. Defaults to "error".

        Returns:
            _type_: _description_
        """

        d = Path(path)
        data = None

        if d.is_dir():

            # ----- Directory Does Exists! -----#
            # - Clear
            if not self.dry_run and clear :
                d.rmdir()

            # - Load
            else :
                data = list(d.iterdir())

        else:

            # ----- Directory Does Not Exists! -----#
            # - Make
            if not self.dry_run and no_exist == "make":
                d.mkdir()

            # - Error
            elif no_exist == 'error' :
                sys.exit("ERROR: '" + str(d.absolute()) + "' does not Exist")

        return d, data


    def get_latest_strtime_dir(self, d) :
        """_summary_

        Args:
            p (_type_): _description_

        Returns:
            _type_: _description_
        """
        print(d)
        list_of_files = list(d.glob("*"))
        latest =  max( [int(Path(x).stem) for x in list_of_files] )
        return str(latest)


    def import_pwds (self, path, delim) :
        """_summary_

        Args:
            path (_type_): _description_
            delim (_type_): _description_

        Returns:
            _type_: _description_
        """
        pwds = {}

        with open(path, encoding="utf-8") as infile:

            # csv reader object constructed from file and given delimiter. 
            reader = csv.reader( infile, delimiter=delim)

            # Load lines into object
            next(reader)

            data = [ tuple(row) for row in reader ]

            # create domain crendentials dictionary 
            for row in data :
                domain = row[0]
                username = row[1]
                password = row[2]
                pwds[ domain ] = { "usr":username, "pwd":password }

        return pwds


    def read(self, p) :
        """_summary_

        Args:
            p (_type_): _description_

        Returns:
            _type_: _description_
        """
        with p.open(mode='r', encoding="utf-8") as infile:
            # Json
            if p.suffix == ".json":
                data=json.load(infile)
            # yaml
            elif p.suffix in [".yaml", ".yml"]:
                data = yaml.safe_load(infile)


            # text
            elif p.suffix in [".txt", ".text"]:
                data = infile

            # undefined
            else: 
                sys.exit("Error: file extension "+str(p.suffix)+" is not supported for read!" )

            return data


    def write(self, p, data) :
        """_summary_

        Args:
            p (_type_): _description_
            data (_type_): _description_
        """

        with p.open(mode='w+', encoding="utf-8") as outfile:

            # json
            if p.suffix == ".json":
                json.dump(data,outfile)

            # yaml
            elif p.suffix == ".yml":
                yaml.dump(data,outfile)

            # text
            elif p.suffix in [".txt", ".text", ".html", ".csv"]:
                if isinstance(data,bytes):
                    p.write_bytes(data)
                elif isinstance(data,str):
                    p.write_text(data, encoding="utf-8")
                else:
                    sys.exit()

            # undefined
            else: 
                sys.exit("Error: file extension "+str(p.suffix)+" is not supported for write!" )




class SinglePather(Pather):
    """_summary_

    Args:
        Pather (_type_): _description_
    """


    parent_dir = None
    fext       = None
    fname      = None
    path       = None
    content    = None


    def gen_path(self):
        """_summary_
        """

        p = self.parent_dir.joinpath(self.fname+self.fext)
        self.path = p


    def write_to_path(self):
        """_summary_
        """

        self.gen_path()
        self.write(self.path,self.content)
