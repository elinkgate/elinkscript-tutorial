import os
from enum import IntEnum, Enum


class FileType(IntEnum):
    TYPE_FILE = 0
    TYPE_DIR = 1


class Entry:
    def __init__(self, entryObj: list):
        self.name = entryObj[0]
        self.type = entryObj[1]
        self.size = entryObj[2]
        self.fullpath = None

    def show(self):
        print("Entry name: {:20} Entry type: {:4} Entry size: {:10}".format(self.name, self.type, self.size))
        if self.fullpath:
            print("Full path: {:30}".format(self.fullpath))

    def setFullPath(self, fullPath: str):
        self.fullpath = fullPath


class FileManager:
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_size(self):
        return self.size

    def __init__(self, elinkObj):
        self._elink = elinkObj

    def entry_list(self, entry=None):
        if entry is None:
            print("entry {} ".format(entry))
            entryList = self._elink.remoteFileList()
        else:
            print("entry {} ".format(entry))
            entryList = self._elink.remoteFileList(entry)
        entries = []
        for obj in entryList:
            element = Entry(obj)
            if entry is None:
                element.setFullPath(element.name)
            else:
                element.setFullPath(entry + "/" + element.name)
            element.show()
            entries.append(element)
        return entries

    def is_file_exist_regress(self, filename: str, entrypoint=None):
        """
        :return entry file path or None
        """
        entrylist = self.entry_list(entrypoint)
        if entrylist is None:
            return None
        for entry in entrylist:
            print(("entry: {}".format(entry.name)))
            print("type of entry.name {}".format(type(entry.name)))
            if entry.name == filename:
                entrypoint = entrypoint.replace("/", "")
                # return "{}/{}".format(entrypoint, entry.name)
                entry.setFullPath("/{}/{}".format(entrypoint, entry.name))
                return entry
            else:
                if entry.type == FileType.TYPE_DIR:
                    return self.is_file_exist_regress(entrypoint="/{}".format(entry.name), filename=filename)
            pass
        return None

    def upload_file(self, srcfile: str, des: str):
        if os.path.isfile(srcfile) is False:
            raise Exception("not found file {}".format(srcfile))
        self._elink.remoteFileUpload(srcfile, des)

    def list_file(self, des: str):
        entries = self.entry_list(des)
        for entry in entries:
            print("{} \t\t {} \t {}".format(entry.name, entry.type, entry.size))

    def remove_file(self, entry: Entry):
        if entry.fullpath is None:
            return
        entryList = self._elink.remoteFileList(entry.fullpath)
        if len(entryList) == 0:
            return
        self._elink.remoteFileDelete(entry.fullpath)
        pass

    def get_md5(self, filepath: str):
        print("not implemented yet")
        return None
