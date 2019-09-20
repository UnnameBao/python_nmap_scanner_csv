# python_nmap_scanner_csv
主要是因为工作需要，写了一个利用python-nmap来批量扫描端口的小工具
使用方法:
```
python3 nmap_scanner.py -i <inputfile> -s <startline> -n <number of lines> -o <outputfile>
```
还是解释一下吧
-i 或者 --input 后面跟随要处理的文件的路径，这个格式呢，就是一个ip地址占一行。

-s 或者 --start 就是从第几行开始，因为要处理的ip可能会很多，扫描时间又很短，中断的话可以从上次中断的地方开始。我会输出一个文件scan.log来记录上次是扫描了多少，下次-s从这里开始就行。不填的话默认是0。

-n 或者 --number 就是扫描几行，还是因为上面的原因嘛，所以有可能一次就扫描几个ip地址，所以可以修改。不填的话默认是10000。

-o 或者 --output 后面跟随要生成的文件的路径，这个会输出一个csv。

这个工具其实很简单，没有设置nmap的参数以及csv格式什么的，不过大框架是差不多的。算是给自己做个记录，也方便大家修改。