这是我的个人仓库，用来存放我使用PMEAL团队开发的开源库OpenPNM、PoreSpy练习的示例。

非常感谢PMEAL小组的工作，它使我的模拟变得容易接受！

OpenPNM的可视化模块做的非常好！PoreSpy有许多应用于2D图像的统计函数，像两点相关函数、弦长分布函数等，十分有用！

截至2023年3月，我使用OpenPNM==3.1.1，PoreSpy==2.2.2

以下是我练习示例：

<<<<<<< HEAD
1.<2D单相流>：创建了40401的网格，模拟了压汞曲线（以及考虑捕集的情况），设置了StokesFlow以进行压力可视化，绘制X方向的压降曲线并预测渗透率。

2.<PNM前处理>：导入3D-PNM，修剪不连通的孔隙，删除网络中多余的键，最终以pbz2的形式压缩存储。

3.<PNMtrimming_Kabs>：解压pbz2文件，设置了StokesFlow以进行压力可视化，绘制X方向的压降曲线并预测渗透率。
=======
1.<2D单相流>：创建了40*40*1的网格，模拟了压汞曲线（以及考虑捕集的情况），设置了StokesFlow以进行压力可视化，绘制X方向的压降曲线并预测渗透率。

2.<PNMtrimming_Kabs>：导入了自己的3D-PNM，修剪不连通的孔隙，设置了StokesFlow以进行压力可视化，绘制X方向的压降曲线并预测渗透率。
>>>>>>> c219d7b5ee46a3e72501276cd361c76832b32c1b
