from os import path
from enum import IntEnum, Enum
from pathlib import Path


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

    def __isDirectoryType__(self, curpath: str):
        entry = self.find_entry(curpath)
        if entry.type == FileType.TYPE_DIR:
            return True
        return False

    def __isFileType__(self, curpath: str):
        entry = self.find_entry(curpath)
        if entry.type == FileType.TYPE_FILE:
            return True
        return False

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

    def get_entry_info(self, entryPath=None):
        """

        :rtype: object
        """
        if entryPath is None:
            print("entry {} ".format(entryPath))
            entryList = self._elink.remoteFileList()
        else:
            print("entry {} ".format(entryPath))
            entryList = self._elink.remoteFileList(entryPath)
        if len(entryList) == 0:
            return None
        else:
            entry = Entry(Entry(entryList[0]))
            return entry

    def find_entry(self, filename: str, entrypoint=None):
        """
        :return entry file path or None
        """
        entrylist = self.entry_list(entrypoint)
        if entrylist is None:
            return None
        for entry in entrylist:
            print(("Entry: {:20} type: {:5}".format(entry.name, entry.type)))
            if entry.name == filename:
                entrypoint = entrypoint.replace("/", "")
                entry.setFullPath("/{}/{}".format(entrypoint, entry.name))
                return entry
            else:
                if entry.type == FileType.TYPE_DIR:
                    return self.find_entry(entrypoint="/{}".format(entry.name), filename=filename)
            pass
        return None

    def upload_file(self, srcfile: str, des: str):
        """

        :param srcfile:
        :param des: directory
        """
        if path.isfile(srcfile) is False:
            raise Exception("not found file {}".format(srcfile))
        self.find_entry(des)
        self._elink.remoteFileUpload(srcfile, des)

    def list_file(self, des: str):
        entries = self.entry_list(des)
        for entry in entries:
            print("{:20} {:2} {:10}".format(entry.name, entry.type, entry.size))

    def remove_file(self, entry: Entry):
        if entry.fullpath is None:
            return
        if self.get_entry_info(entry.fullpath) is None:
            return
        self._elink.remoteFileDelete(entry.fullpath)
        pass

    def rename_entry(self, entry: Entry, newname: str):
        myEntry = self.find_entry(entry.name, entrypoint=entry.fullpath)
        if myEntry is None:
            return
        dirname = path.dirname(newname)
        dir = self.get_entry_info(dirname)
        if dir is None:
            return
        if dir.type != FileType.TYPE_DIR:
            return
        self._elink.remoteRenameFile(entry.fullpath, newname)
        pass

    def get_md5(self, filepath: str):
        print("not implemented yet")
        return None
