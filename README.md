Clip Board To File
=====
We like copy and paste. but normally os can only maintain the latest copied content. So we need copy & paste again and again.
So I introduce this little GUI tools, it will continuously monitor your clip board and save the content to your file.
在拷贝粘贴的操作中，操作系统一般只保留最新的一份，因此，我们要不断的重复拷贝-粘贴的动作，本小工具可以持续的监控你系统的剪贴板的内容，并讲这些内容拷贝到你指定的问件中。


Feature
====
#####Monitoring you clip board and save the new content to file
#####support key words filter and replace ,this is very useful when you handle the url


Support
====
OS:windows
Python : python 3

Installation
====
### step 1. down load the tools
### step 2. edit the configuration
    [DEFAULT]
    ;the original key word
    sourcestr =
    ;the target key word, such as you want replace all http with https: sourcestr = http   targetstr = https
    targetstr =
    ;the path of your saved file
    savepath = C:/mydownloads
    ;the name of your saved file
    targetfile = mynote
    ;filter, the tool will copy only start with the key words, such as, you can set keywords = https, so only content
    ;started with https will be copied.
    keywords =
### step 3 run
    python you\file\path\ClipbrdToFile.py
