using UnityEngine;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Data;
using System.Linq;

public class playercontrol : MonoBehaviour {

	/*
	 * D-PAD -
	 *  left down: a
	 *  left up:   q
	 * 
	 *  right down: d
	 *  right up:   c
	 * 
	 *  up, up:    w
	 *  up, down:  e
	 * 
	 *  down up:   x
	 *  down down: z
	 * 
	 *  left trigger down: h
	 *  left trigger up:   r
	 * 
	 *  right trigger down: j
	 *  right trigger up:   n
	 * 
	 *  select up:    y
	 *  select down:  t
	 * 
	 *  start up:     u
	 *  start down:   f
	 * 
	 *  leftbottom up:   k 
	 *  leftbottom down: p
	 * 
	 *  rightbottom up:  l
	 *  rightbttom down: v
	 * 
	 *  lefttop up:    i
	 *  lefttop down:  m
	 * 
	 *  righttop up:   o
	 *  righttop down: g
	 * 
	 * 
	 */ 

	char[] DP_Left  = { 'a', 'q' };
	char[] DP_Right = { 'd', 'c' };
	char[] DP_Up    = { 'w', 'e' };
	char[] DP_Down  = { 'x', 'z' };

	char[] BSelect = { 'y', 't' };
	char[] BStart  = { 'u', 'f' };

	char[] LeftTrigger  = { 'h', 'r' };
	char[] RightTrigger = { 'j', 'n' };

	char[] UpperLeft  = { 'i', 'm' };
	char[] UpperRight = { 'd', 'g' };
	char[] LowerLeft  = { 'k', 'p' };
	char[] LowerRight = { 'l', 'v' };

	bool ButtonDownDPad = false;

	bool ButtonDownSelect = false;
	bool ButtonDownStart = false;

	bool ButtonDownLeftTrigger = false;
	bool ButtonDownRightTrigger = false;

	bool ButtonDownUpperLeft = false;
	bool ButtonDownUpperRight = false;
	bool ButtonDownLowerLeft = false;
	bool ButtonDownLowerRight = false;

	// movement bools
	bool Moving = false;
	bool MovingLeft = false;
	bool MovingRight = false;
	bool MovingUp = false;
	bool MovingDown = false;
	bool StopMoving = false;
	bool Jumping = false;

	float xvelocity;
	float yvelocity;

	float MovementSpeed = 8f;

	Vector3 directions = new Vector3(0, 0, 0);

	IEnumerator Movements() {
		while (true) {

			//this.rigidbody.velocity = directions;
			//this.transform.Translate(Vector3.left * Time.deltaTime * MovementSpeed);
			//this.transform.Translate(Vector3.up * Time.deltaTime * MovementSpeed);
			//this.rigidbody.AddForce(direction);

			//if (Jumping == true) {  }//this.rigidbody.velocity = new Vector3(0, 10, 0); }

			//if (MovingLeft == true) { xvelocity = -10; } //this.rigidbody.velocity = new Vector3(-10, 0, 0); }
			//if (MovingRight == true) { xvelocity = 10; } //this.rigidbody.velocity = new Vector3(10, 0, 0); }

			//if (StopMoving == true) {
				//this.rigidbody.velocity = new Vector3(0, 0, 0); 
			//	xvelocity = 0;
			//	yvelocity = 0;

			//	StopMoving = false;
			//}

			//this.rigidbody.velocity = new Vector3(xvelocity, 0, 0);
			//this.rigidbody.velocity = new Vector3(xvelocity, yvelocity, 0);
			//this.rigidbody.AddForce (xvelocity, yvelocity, 0);


			//if (this.rigidbody.velocity.x >= 10) {

			//}



			yield return new WaitForFixedUpdate(); //WaitForEndOfFrame();
		}

	}

	void Start() {


		//StartCoroutine(Movements ());
	}

	void Update() {
		if (Input.GetKeyDown(DP_Left[0].ToString())) {
			ButtonDownDPad = true;
			directions.x = -25;
		}
		if (Input.GetKeyUp(DP_Left[1].ToString())) {
			ButtonDownDPad = false;
			//directions.x = 0;
			var yvel = this.rigidbody.velocity.y;
			this.rigidbody.velocity = new Vector3(0, yvel, 0);
		}

		if (Input.GetKeyDown(DP_Right[0].ToString())) {
			ButtonDownDPad = true;
			directions.x = 25;
		}
		if (Input.GetKeyUp(DP_Right[1].ToString())) {
			ButtonDownDPad = false;
			//directions.x = 0;
			var yvel = this.rigidbody.velocity.y;
			this.rigidbody.velocity = new Vector3(0, yvel, 0);
		}
		//foreach (char c in Input.inputString) {
			//print (c);
			//if (c == DP_Left[0]) { /// holding down LEFT on dpad
			//		ButtonDownDPad = true;
			//		print("GOIN LEFT");
					//this.rigidbody.AddForce(10, 0, 0);
			//}

			//if (c == DP_Left[1]) { /// releaseing LEFT on dpad
					//ButtonDownDPad = false;
			//		print ("STOPED GOIN LEFT");
				//this.rigidbody.velocity = new Vector3(0,0,0);
			//}

		//}

	}
	void FixedUpdate() {
		print (this.rigidbody.velocity);

		this.rigidbody.AddForce(directions);

		var xveloc = this.rigidbody.velocity;
		if (xveloc.x >= 25) {
			this.rigidbody.velocity = new Vector3(25, this.rigidbody.velocity.y, 0);
		}
		else if (xveloc.x <= -25) {
			this.rigidbody.velocity = new Vector3(-25, this.rigidbody.velocity.y, 0);
		}

	}
	/* 
	// Update is called once per frame
	void Update () {


		foreach (char c in Input.inputString) {
			//print("1 "+ c);

			//DIRECTIONAL PAD
			// button up
			if (ButtonDownDPad == false) {
				if (c == DP_Left[0]) {
					//action here
					///// MOVE LEFT
					ButtonDownDPad = true;
					//Moving = true;
					MovingLeft = true;
					MovingRight = false;
					//directions.x = -10;
					//this.rigidbody.velocity = 
					//this.transform.Translate (new Vector3(-10,0,0) * Time.deltaTime*1);
					//print ("wat");
					//StartCoroutine(MoveLeft());
					//print ("lefting");
				}
				if (c == DP_Right[0]) {
					//action here
					///// MOVE RIGHT
					ButtonDownDPad = true;
					MovingLeft    = false;
					MovingRight   = true;
					//directions.x = 10;
					//StartCoroutine(MoveRight());
				}
				if (c == DP_Up[0]) {
					//action here
					///// CLIMB UP
					ButtonDownDPad = true;
				}
				if (c == DP_Down[0]) {
					//action here
					///// CLIMB DOWN
					ButtonDownDPad = true;
				}
			}
			// button down
			else if (ButtonDownDPad == true) {
				if (c == DP_Left[1]) {
					//action here
					ButtonDownDPad = false;
					//Moving = false;
					MovingLeft = false;
					StopMoving = true;
					print ("left done");
				}
				if (c == DP_Right[1]) {
					//action here
					ButtonDownDPad = false;
					MovingRight   = false;
					StopMoving = true;
				}
				if (c == DP_Up[1]) {
					//action here
					ButtonDownDPad = false;
				}
				if (c == DP_Down[1]) {
					//action here
					ButtonDownDPad = false;
				}
			}

			// SELECT BUTTON
			if (ButtonDownSelect == false) {
				if (c == BSelect[0]) {
					ButtonDownSelect = true;
				}
			}
			else if (ButtonDownSelect == true) {
				if (c == BSelect[1]) {
					ButtonDownSelect = false;
				}
			}

			// START BUTTON
			if (ButtonDownStart == false) {
				if (c == BStart[0]) {
					ButtonDownStart = true;
				}
			}
			else if (ButtonDownStart == true) {
				if (c == BStart[1]) {
					ButtonDownStart = false;
				}
			}

			// LEFT TRIGGER
			if (ButtonDownLeftTrigger == false) {
				if (c == LeftTrigger[0]) {
					ButtonDownLeftTrigger = true;
				}
			}
			else if (ButtonDownLeftTrigger == true) {
				if (c == LeftTrigger[1]) {
					ButtonDownLeftTrigger = false;
				}
			}

			// RIGHT TRIGGER
			if (ButtonDownRightTrigger == false) {
				if (c == RightTrigger[0]) {
					ButtonDownRightTrigger = true;
				}
			}
			else if (ButtonDownRightTrigger == true) {
				if (c == RightTrigger[1]) {
					ButtonDownRightTrigger = false;
				}
			}

			// Upper Left
			if (ButtonDownUpperLeft == false) {
				if (c == UpperLeft[0]) {
					ButtonDownUpperLeft = true;
				}
			}
			else if (ButtonDownUpperLeft == true) {
				if (c == UpperLeft[1]) {
					ButtonDownUpperLeft = false;
				}
			}

			///// JUMP BUTTON
			//Upper Right
			if (ButtonDownUpperRight == false) {
				if (c == UpperRight[0]) {
					ButtonDownUpperRight = true;
					Jumping = true;
				}
			}
			else if (ButtonDownUpperRight == true) {
				if (c == UpperRight[1]) {
					ButtonDownUpperRight = false;
					Jumping = false;
				}
			}

			// Lower Left
			if (ButtonDownLowerLeft == false) {
				if (c == LowerLeft[0]) {
					ButtonDownLowerLeft = true;
				}
			}
			else if (ButtonDownLowerLeft == true) {
				if (c == LowerLeft[1]) {
					ButtonDownLowerLeft = false;
				}
			}

			///// ATTACK BUTTON
			//Lower Right
			if (ButtonDownLowerRight == false) {
				if (c == LowerRight[0]) {
					ButtonDownLowerRight = true;
				}
			}
			else if (ButtonDownLowerRight == true) {
				if (c == LowerRight[1]) {
					ButtonDownLowerRight = false;
				}
			}




			this.rigidbody.velocity = directions;














		}
		//yield return new WaitForEndOfFrame();
	}*/


}


