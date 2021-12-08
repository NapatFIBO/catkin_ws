#!/usr/bin/env python3

import rospy
import pyaudio
import time
import speech_recognition as sr

# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
# from enum import Enum

# class RoomStation(Enum):
#     Start = 0
#     Room1_pos1 = 1
#     Room1_pos2 = 2
#     Room1_pos3 = 3
#     Room1_pos4 = 4
#     Room2_pos1 = 5
#     Room2_pos2 = 6
#     Room2_pos3 = 7
#     Room2_pos4 = 8
#     Room3_pos1 = 9
#     Room3_pos2 = 10
#     Room3_pos3 = 11
#     Room3_pos4 = 12
#     Room4_pos1 = 13
#     Room4_pos2 = 14
#     Room4_pos3 = 15
#     Room4_pos4 = 16


r = sr.Recognizer()
diff_state = 3

KeyWord = { "ไปห้อง 1":"Room_1",
            "ไปห้อง 2":"Room_2",
            "ไปห้อง 3":"Room_3",
            "ไปห้อง 4":"Room_4"}



Goal = {"Room_1":[[2.8143,-5.9862,-0.0052,1],[6.2153,-5.3899,-0.9377,0.3473],[3.8321,-7.1192,-0.8326,0.5539],[2.7611,-9.7242,0.7037,0.7105]],
        "Room_2":[[-0.568,-6.1497,0.9986,0.0529],[-3.7021,-6.087,-0.7108,0.7034],[-3.8691,-8.7927,-0.1725,0.985],[-1.6652,-9.6777,0.6987,0.7154]],
        "Room_3":[[2.8797,-2.5876,-0.0316,0.9995],[6.2866,-2.961,0.7034,0.7108],[6.058,0.3616,0.9961,0.0885],[3.9744,0.8585,-0.7165,0.6975]],
        "Room_4":[[-0.4737,-2.5148,-0.7108,0.7034],[-0.4275,-0.0176,-0.9943,0.1064],[-3.4625,0.5676,-0.7303,0.6831],[-3.7833,-3.6105,-0.0104,0.9999]]}




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
            try:
                rospy.loginfo("Setting MIC: Say Something . . .")
                with sr.Microphone() as source:
                    audio = r.listen(source)
                    word = r.recognize_google(audio,language='th')
                    rospy.loginfo("Mic testing . . . STATUS: OK")
                    break

            except:
                rospy.loginfo("Setting MIC: Say Something . . .")



        while 1:
            if (diff_state == 0):
               rospy.loginfo("ready to get command")
               diff_state = 1

            elif (diff_state == 1):  
                try:
                    with sr.Microphone() as source:                
                        audio = r.listen(source)
                        word = r.recognize_google(audio,language='th')
                        try:
                            rospy.loginfo("Going to . . . " + KeyWord[word])
                            for i in range(3):
                                result = movebase_client(Goal[KeyWord[word[i]]])

                            result = movebase_client(Goal[KeyWord[word[i]]])
                            if result:
                                rospy.loginfo("Arrive at desired room")
                                diff_state = 2
                        except:
                            rospy.loginfo("Can't decode your voice,say again pls")
                            rospy.loginfo("Command Example : ไปห้อง 1")
                            pass

                except:
                    pass

            elif (diff_state == 2):  
                rospy.loginfo("Wait for customer interaction . . .")
                time.sleep(10)
                rospy.loginfo("Back to Standby-Station")
                diff_state = 3
            
            elif (diff_state == 3):
                rospy.loginfo("Going to . . . Standby_Station")
                result = movebase_client(Goal["Room_4"[0]])
                if result:
                    rospy.loginfo("Arrive at the Standby-Station")
                    rospy.loginfo("Standby for Command !!!")
                    diff_state = 0
            




    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
