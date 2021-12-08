# FRA502 ROS FINAL PROJECT 
## Develop by
Mr. Napat Suwanaksorn

ID:62340500016
## Video link : 
https://drive.google.com/drive/folders/1t2_-zJRBF0eF6T8HFLFMkPVAPhJRcjOz?usp=sharing
## คู่มือการใช้งาน : 
1. ทำการlaunch file ชื่อ all_in_one.launch ด้วยคำสั่ง roslaunch diff_drive all_in_one.launch เพื่อทำการ เปิด gazebo ,spawn robot ,navigation และเปิด rviz 
2. ทำการสั่งคำสั่งเสียงผ่าน terminal ด้วย python โดยใช้คำสั่ง rosrun diff_drive test.py 
3. ทำการสั่งการด้วยเสียงเป็นภาษาไทยเพื่อไปยังห้องต่าง ๆ โดยใช้คำสั่งว่าไปที่ห้องหมายเลขไหน โดยเมื่อหุ่ยนต์ไปถึงห้องนั้นหุ่นยนต์จะเดินไปตามตำแหน่งที่ตั้งไว้ภายในห้อง ซึ่งในแต่ละห้องจะมีห้องละ 4 จุด เพื่อพ่นยาฆ่าแมลงและทำการแจ้งเตือนในแต่ละจุดว่า Point x Success โดยหุ่นยนต์จะรอรับคำสั่งของผู้ใช้ตลอดเวลา
## ปัญหาที่พบเจอ ในช่วงแรกที่ใช้ Ubuntu ทางผมได้ใช้เป็น Oracle VM VirtualBox ซึ่งปัญหาที่พบจะมีดังนี้
1. เมื่อทำการใช้งาน gazebo แล้วพบว่าเมื่อทำการ save world แล้วทำการเปิด world ที่ได้บันทึกไว้ ปรากฎว่า world นั้นเป็นสีดำโดยเมื่อทำการรอเป็นเวลานานก็ไม่ขึ้น
2. laser scan ไม่สามารถใช้งานได้ สืบเนื่องมาจากปัญหาการ์ดจอที่ virsual box ไม่สามารถใช้งานการ์ดจอได้มีประสิทธิภาพเท่าการลง dual boot
3. ความยากลำบากในการจูนค่า parameters ต่าง ๆ
4. หุ่นไม่ค่อยเดินตาม path ที่หุ่นได้วางเอาไว้
