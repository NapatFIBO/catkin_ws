#!/usr/bin/env python3

import rospy
import pyaudio
import time
import speech_recognition as sr

# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

r = sr.Recognizer()
diff_state = 0
process = 1
KeyWord = { "ห้อง 1":"Room_1",
            "ห้อง 2":"Room_2",
            "ห้อง 3":"Room_3",
            "ห้อง 4":"Room_4",
            "ช่อง 1":"Room_1",
            "ช่อง 2":"Room_2",
            "ช่อง 3":"Room_3",
            "ช่อง 4":"Room_4",
            "คลอง 1":"Room_1",
            "คลอง 2":"Room_2",
            "คลอง 3":"Room_3",
            "คลอง 4":"Room_4",
            "ห้องที่ 1":"Room_1", 
            "ห้องที่ 2":"Room_2",
            "ห้องที่ 3":"Room_3",
            "ห้องที่ 4":"Room_4"}

Goal = {"Room_1":[2.8143,-5.9862,-0.0052,1],
        "Room_1p2" :[6.2153,-5.3899,-0.9377,0.3473],
        "Room_1p3" :[3.8321,-7.1192,-0.8326,0.5539],
        "Room_1p4" :[2.7611,-9.7242,0.7037,0.7105],
        "Room_2":[-0.568,-6.1497,0.9986,0.0529],
        "Room_2p2" :[-3.7021,-6.087,-0.7108,0.7034],
        "Room_2p3" :[-3.8691,-8.7927,-0.1725,0.985],
        "Room_2p4" :[-1.6652,-9.6777,0.6987,0.7154],
        "Room_3":[2.8797,-2.5876,-0.0316,0.9995],
        "Room_3p2" :[6.2866,-2.961,0.7034,0.7108],
        "Room_3p3" :[6.058,0.3616,0.9961,0.0885],
        "Room_3p4" :[3.9744,0.8585,-0.7165,0.6975],
        "Room_4":[-0.4737,-2.5148,-0.7108,0.7034],
        "Room_4p2" :[-0.4275,-0.0176,-0.9943,0.1064],
        "Room_4p3" :[-3.4625,0.5676,-0.7303,0.6831],
        "Room_4p4" :[-3.7833,-3.6105,-0.0104,0.9999]}

def movebase_client(map_odom_desire):

   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
 
   # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

   # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = map_odom_desire[0]
    goal.target_pose.pose.position.y = map_odom_desire[1]
    goal.target_pose.pose.orientation.z = map_odom_desire[2]
    goal.target_pose.pose.orientation.w = map_odom_desire[3]

   # Sends the goal to the action server.
    client.send_goal(goal)
   # Waits for the server to finish performing the action.
    wait = client.wait_for_result()
   # If the result doesn't arrive, assume the Server is not available
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
    # Result of executing the action
        return client.get_result()   

# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    try:
       # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        rospy.init_node('movebase_client_py')

        while 1:
            if (diff_state == 0):
               print("ready to get voice command")
               diff_state = 1

            elif (diff_state == 1):  
                try:
                    with sr.Microphone() as source:             
                        print("say")   
                        audio = r.listen(source,phrase_time_limit=10)
                        print("stop")
                        word = r.recognize_google(audio,language='th')
                        print(word)
                        try:
                            print("Going to . . . " + KeyWord[word])
                            result = movebase_client(Goal[KeyWord[word]])
                            if result:
                                print("Point 1 Success.")
                                for i in range(2,5):
                                    try:
                                        result = movebase_client(Goal[KeyWord[word]+"p"+str(i)])
                                        if result:
                                            print("Point "+str(i) +" Success.")
                                    except:
                                        pass
                        except:
                            print("Can't decode your voice,please try again.")
                            print("Command Example : Goal => 1 ,Say : ห้อง 1")
                            pass
                except:
                    pass
            
    except rospy.ROSInterruptException:
        print("Navigation test finished.")
