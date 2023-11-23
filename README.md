这是我的个人仓库，用来存放我使用PMEAL团队开发的开源库OpenPNM、PoreSpy练习的示例。

非常感谢PMEAL小组的工作，它使我的模拟变得容易接受！

OpenPNM的可视化模块做的非常好！PoreSpy有许多应用于2D图像的统计函数，像两点相关函数、弦长分布函数等，十分有用！

截至2023年3月，我使用OpenPNM==3.1.1，PoreSpy==2.2.2

以下是我练习示例：

1.<2D单相流>：创建了40*40的网格，模拟了压汞曲线（以及考虑捕集的情况），设置了StokesFlow以进行压力可视化，绘制X方向的压降曲线并预测渗透率。

2.<PNM前处理>：导入3D-PNM，修剪不连通的孔隙，删除网络中多余的键，最终以pbz2的形式压缩存储。

3.<PNM_Kabs>：解压pbz2文件，设置了StokesFlow以进行压力可视化并预测渗透率。

4.<SNOW>：导入2D/3D.tif图像，使用SNOW算法提取其PNM并可视化。
