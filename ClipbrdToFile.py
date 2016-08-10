#!/usr/bin/python
# -*- coding: utf-8 -*-
########################################################################
# Name:
# 		ClipbrdToFile.py
# Description:
# 		GUI tools, it will continuously monitor your clip board and save the content to your file.
# Author:
# 		wuwesley
# Python:
#       3.0+
# Version:
#		1.0
########################################################################
__author__ = 'wuwesley'

from tkinter import *
import os
import tkinter.messagebox as messagebox
import configparser

class ClipbrdToFile:

    def __init__(self):
        self.tk = Tk()
        self.tk.geometry('350x350+300+300')
        self.tk.resizable(0, 0)
        self.tk.title('Clipboard Watcher By Wesley')

        # define the configuration file
        self.confPath = "clipbrdtofile.cfg"
        self.frame = Frame(self.tk, relief=RAISED, height=10, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=0)

        # initialise the configuration
        self.init_config_file()
        self.update_global_var()
        #
        # Adding Text Widget & ScrollBar widget
        #
        self.filenote = Label(self.frame, text="File:")
        self.filenote.pack(side=LEFT,padx=3, pady=3)
        self.filename = Entry(self.frame, width=10)
        self.filename.insert(0, self.mTargetFile)
        self.filename.pack(side=LEFT,padx=3, pady=3)
        self.pathnote = Label(self.frame, text="Path:")
        self.pathnote.pack(side=LEFT,padx=3, pady=3)
        self.savepath = Entry(self.frame, width=18)
        self.savepath.insert(0, self.mSavePath)
        self.savepath.pack(side=LEFT,padx=3, pady=3)
        self.changefile = Button(self.frame,text="Change",command=self.update_targetfile_value)
        self.changefile.pack(side=RIGHT,padx=3, pady=3)
        self.textPad = Text(self.tk, undo=True)
        self.textPad.pack(expand=YES, fill=BOTH)
        self.scroll=Scrollbar(self.textPad)
        self.textPad.configure(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.textPad.yview)
        self.scroll.pack(side=RIGHT,fill=Y)
        #self.textPad.insert(END, self.tk.clipboard_get())
        self.last_content = ''
        self.tk.after(100, self.watch_clipboard)
        self.tk.mainloop()

    # the main logic, watching the clipboard change event
    def watch_clipboard(self):
        try:
            content = self.tk.clipboard_get()
            if content != self.last_content:
                self.last_content = content
                self.textPad.delete(1.0, END)
                self.textPad.insert(END, self.last_content)
                self.append_to_file()
                #self.tk.clipboard_clear()
                #messagebox.showinfo('Refreshed')
        except TclError:
            pass
        self.tk.after(300, self.watch_clipboard)

    # initialize the configuration file, put the default setting, currently support below keys
    # TargetFile, the file which will store the content from the clipboard
    # KeyWords, the key word which will be used to filter the content.i.e the string contain 'http' will be processed
    # SourceStr, the source string that will be replaced in the original content
    # TargetStr, the final string that will be used in the final content
    def init_config_file(self):
        if os.path.exists(self.confPath):
            return
        mConfig = configparser.ConfigParser()
        mConfig['DEFAULT'] = {'TargetFile': '',
                              'KeyWords': '',
                              'SourceStr': '',
                              'SavePath': '',
                              'TargetStr': ''}
        with open(self.confPath, 'w') as configfile:
             mConfig.write(configfile)

    # read and update the global variable in memory
    def update_global_var(self):
        self.mTargetFile = self.read_config_by_key('TargetFile')
        self.mKeyWords = self.read_config_by_key('KeyWords')
        self.mSourceStr = self.read_config_by_key('SourceStr')
        self.mTargetStr = self.read_config_by_key('TargetStr')
        self.mSavePath = self.read_config_by_key('SavePath')
        self.mHasTargetFile = False

    # append teh content of the clipboard to the specific file, currently support below key
    def append_to_file(self):
        newFileName = self.mTargetFile
        if self.mSavePath != '':
            newFileName = self.mSavePath + '/' + self.mTargetFile
        newKeyWords = self.mKeyWords
        # do nothing if the file name or content is NULL
        if newFileName == '' or self.last_content == '':
            return
        #messagebox.showinfo(self.last_content)
        #messagebox.showinfo(newKeyWords)
        #messagebox.showinfo(self.last_content.find(newKeyWords))

        # filter the content by the keywords
        if newKeyWords != '' and self.last_content.find(newKeyWords) == -1:
            return

        # begin to process the file
        try:
            conPathHandler = open(newFileName, "a")
            try:
                mContent = self.process_the_content()
                if mContent!='' :
                    conPathHandler.write(mContent + "\n")
            finally:
                conPathHandler.close()
                return newFileName
        except IOError:
            pass

    # read the specific key from the configuration file
    def read_config_by_key(self,mKey):
        mConfig = configparser.ConfigParser()
        mConfig.read(self.confPath)
        return mConfig.get('DEFAULT', mKey)

    # update the TargetFile value
    def update_targetfile_value(self):
        newFileName = self.filename.get().strip()
        newSavePath = self.savepath.get().strip()
        if newFileName == '' or newSavePath == '':
            self.show_message_info("The filename or savepath does not exists!")
            return
        newSavePath = self.savepath.get().replace("\\","/")
        mConfig = configparser.ConfigParser()
        mConfig.read(self.confPath)
        if mConfig.has_option('DEFAULT', 'TargetFile'):
            mConfig.set('DEFAULT', 'TargetFile', newFileName)
            mConfig.set('DEFAULT', 'SavePath', newSavePath)
            with open(self.confPath, 'w') as configfile:
                mConfig.write(configfile)

        # create the file if it does not exist
        #if not os.path.exists(newFileName):
        #     open(newFileName, 'a').close()
        # update the global variables
        self.update_global_var()
        self.mHasTargetFile = True
        # update the gui
        self.filename.delete(0, END)
        self.filename.insert(0, self.mTargetFile)
        self.savepath.delete(0, END)
        self.savepath.insert(0, self.mSavePath)
        # refresh the clipboard
        self.tk.clipboard_clear()
        self.textPad.delete(1.0, END)
        # show the change result
        self.show_message_info("The value of filename or savepath is updated!")

    # update the value for the specific key
    # **keyv : AutoLogin='False'
    def change_config_by_key(self,mKey,**keyv):
        #newFileName = self.filename.get()
        mConfig = configparser.ConfigParser()
        mConfig.read(self.confPath)
        [mConfig.set('DEFAULT', mKey, keyv[mKey]) for mKey in keyv if mConfig.has_option('DEFAULT', mKey)]
        mConfig.write(open(self.confPath, 'w'))

    # find and replace the string before save
    def process_the_content(self):
        sourceStr = self.mSourceStr
        targetStr = self.mTargetStr
        mContent = ''
        if sourceStr == "":
            return self.last_content
        mContent = self.last_content.replace (sourceStr,targetStr)
        return mContent

    # show response message in the bottom text box
    def show_message_info(self, msg):
       self.textPad.delete(1.0, END)
       self.textPad.insert(END, msg)

if __name__ == '__main__':
    mClipbrdToFile = ClipbrdToFile()