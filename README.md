<h1 align="center">python-五子棋</h1>
<div align="center">
  <a href="https://github.com/tctctctctc/python-gobang/stargazers">
    <img src="https://img.shields.io/github/stars/tctctctctc/python-gobang" alt="Stars Badge"/>
  </a>
  <a href="https://github.com/tctctctctc/python-gobang/network/members">
    <img src="https://img.shields.io/github/forks/tctctctctc/python-gobang" alt="Forks Badge"/>
  </a>
  <a href="https://github.com/tctctctctc/python-gobang/pulls">
    <img src="https://img.shields.io/github/issues-pr/tctctctctc/python-gobang" alt="Pull Requests Badge"/>
  </a>
  <a href="https://github.com/tctctctctc/python-gobang/issues">
    <img src="https://img.shields.io/github/issues/tctctctctc/python-gobang" alt="Issues Badge"/>
  </a>
  <a href="https://github.com/tctctctctc/python-gobang/graphs/contributors">
    <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/tctctctctc/python-gobang?color=2b9348">
  </a>
  <a href="https://github.com/tctctctctc/python-gobang/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/tctctctctc/python-gobang?color=2b9348" alt="License Badge"/>
  </a>  
  <br>
  <a href="https://github.com/tctctctctc/python-gobang/blob/master/README.en.md">
    <img src="https://img.shields.io/static/v1?label=&labelColor=505050&message=English README 英文自述文件&color=%230076D6&style=flat&logo=google-chrome&logoColor=green" alt="website"/>
  </a>
  
  <i>喜欢这个项目吗？请考虑给 Star ⭐️ 以帮助改进！</i>
</div>

---

### 1. 简介  
  刚学完Python套接字后做的一个五子棋小游戏，在局域网内可以双人对战，用Pygame加套接字实现,又分为服务器和客户端部分
  在windows环境多次测试均运行正常  
      
### 2. 主要思路

#### 2.1 局域网对战

对于局域网功能来说，首先建立连接（tcp），然后每次下棋时将棋子的坐标发送给对方，当接收到坐标后实例化成棋子对象，这
个接收时用了select函数，因为pygame需要循环渲染图片，所以要用非阻塞方式接收消息

select()的机制中提供一fd_set的数据结构，实际上是一long类型的数组， 每一个数组元素都能与一打开的文件句柄（不管
是Socket句柄，还是其他文件或命名管道或设备句柄）建立联系，建立联系的工作由程序员完成， 当调用select()时，由内核
根据IO状态修改fd_set的内容，由此来通知执行了select()的进程哪一Socket或文件可读或可写，主要用于Socket通信当中

#### 2.2 电脑对战

电脑对战的思路也很简单，用了应该是最常见的也是最简单的方法，就是循环遍历棋盘的每一个点，判断该点的价值，选取价值最
大的点落子，这个需要对五子棋的棋型有一定了解，这里介绍几种常见的棋型（约定1为己方棋子，2为对方棋子，0为空）

    活四（011110）：这时候四颗棋子相连，同时两端为空，已经阻止不了一方的胜利了，此时价值应该设置最高
    死四（011112|10111|11011）：四颗棋子，只有一个地方能形成连五，如果是自己的棋可以赢，是对方的也可以阻止对方赢棋，此时价值次高
    ......
就这样把每种棋型判断一下，获得该点的价值,电脑选择落子位置时，要判断是进攻还是防守，需要两次遍历棋盘，获取进攻时的
最大价值和防守的最大价值

### 3. 游戏截图
![](https://github.com/tctctctctc/python-/raw/master/resouse/a.png)
