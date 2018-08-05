
module eyes() {
	// Background
	color ([0, 0, 0]) 
	resize([0.5, 1, 2])
	sphere (r=1, $fa=1, $fs=0.5);
	
	// White pupil
	color([1, 1, 1])
	translate([0.1, 0, 0.2]) 
	resize([0.5, 0.5, 1.3])
	sphere (r=1, $fa=1, $fs=0.5);
}

module spot() {
	// Yellow body spots
	color([1, 1, 0])
	resize([0.5, 1.5, 4])
	sphere (r=1, $fa=1, $fs=0.5);
}

module head() {
	// Base of the horns
	color([205/255, 133/255, 63/255]) 
	cylinder(r=1, h=6, $fa=1, $fs=0.5);
	
	// Horn articulation point
	color([205/255, 133/255, 63/255]) 
	translate([0, 0, 6]) 
	sphere(r=1, $fa=1, $fs=0.5);
	
	// Left horn
	color([205/255, 133/255, 63/255]) 
	translate([0, 0, 6]) 
	rotate([45, 45, 0])
	difference() {
		cylinder(r1=1, r2=1.5, h=7, $fa=1, $fs=0.5);
		
		translate([0, 0, 2]) 
		cylinder(r=1, h=7.1, $fa=1, $fs=0.5);
	}
	
	// Right horn
	color([205/255, 133/255, 63/255]) 
	translate([0, 0, 6]) 
	rotate([-45, 45, 0])
	difference() {
		cylinder(r1=1, r2=1.5, h=7, $fa=1, $fs=0.5);
		
		translate([0, 0, 2]) 
		cylinder(r=1, h=7.1, $fa=1, $fs=0.5);
	}
	
	// Eyes
	translate([4.4, -1, -4.5])  eyes();
	translate([4.4, 1, -4.5])  eyes();
}

module trunk(top_trunk=12.5, bot_trunk=20, r_trunk=4.5, a_trunk=[-3, 1, 0]) {
	
	// Top Trunk
	rotate(a_trunk) {
		
		// Head, containing eyes and horns
		translate([0, 0, 13.5])
		head();
		
		// Difference to draw the mouth
		color([205/255, 133/255, 63/255])  
		difference() {
			union() {
				// Top trunk
				cylinder(r=r_trunk, h=top_trunk, $fa=1, $fs=0.5);
						
				// Intersection between top and bottom trunk
				sphere(r=r_trunk, $fa=1, $fs=0.5);
			}
			
			translate([5, 0, 6]) 
			scale([1.5, 0.8, 1]) 
			cylinder(r=r_trunk, h=0.8);
		}
		
		// The same than above, but different color for the
		// tongue
		color([227/255, 93/255, 106/255])  
		difference() {
			union() {
				cylinder(r=r_trunk-0.1, h=top_trunk-0.1, $fa=1, $fs=0.5);
						
				// Intersection between top and bottom trunk
				sphere(r=r_trunk-0.1, $fa=1, $fs=0.5);
			}
			
			translate([5, 0, 6.1]) 
			scale([1.5, 0.8, 1]) 
			cylinder(r=r_trunk + 0.1, h=06);
		}
		
		
		// Rounded top cylinder border
		color([205/255, 133/255, 63/255]) 
		translate([0, 0, top_trunk]) 
		resize([2*r_trunk, 2*r_trunk, r_trunk/2]) 
		sphere(r=r_trunk);
		
	}

	//Bot Trunk
	rotate([5, -3, 0]) {
		
		// Bottom trunk
		color([205/255, 133/255, 63/255]) 
		translate([0, 0, -bot_trunk]) {
			cylinder(r=r_trunk, h=bot_trunk, $fa=1, $fs=0.5);
			sphere(r=r_trunk, $fa=1, $fs=0.5);
			
		}
		
		// Front spots
		translate([4.5, 0, -3]) 
		spot();
		
		translate([4, 2, -7]) 
		spot();
		
		translate([3.8, -2, -6.5]) 
		spot();
		
		translate([4.5, -1, -11]) 
		spot();
		
		translate([4, 2, -15]) 
		spot();
		
		// Back spots
		translate([-4.5, 0, -3]) 
		spot();
		
		translate([-4, 2, -7]) 
		spot();
		
		translate([-3.8, -2, -6.5]) 
		spot();
		
		translate([-4.5, -1, -11]) 
		spot();
		
		translate([-4, 2, -15]) 
		spot();
		
		
	}
}

module hand(r_bot=2, r_top=1.8, h=5.1) {
	translate([0.5, 0, h-0.1]) {
		// Begin of the hand
		color([205/255, 133/255, 63/255])
		translate([-0.5, 0, -5]) 
		cylinder(r1=r_bot, r2=r_top, h=h, $fa=1, $fs=0.5);
		
		// Middle finger
		rotate([0, 25, 0]) 
		translate([-0.5, 0, -1]) 
		finger();
		
		//Right Finger
		rotate([-90, 0, -25])
		translate([-1, 2, 1.5])
		finger();
		
		//Left Finger
		rotate([90, 0, 25]) 
		translate([-1, -2, 1.5])
		finger();
		
		// Part behind the hand
		color([205/255, 133/255, 63/255]) 
		resize([3.5, 6, 6]) 
		translate([-1.5, 0, -1.5]) 
		sphere(r=3, $fa=1, $fs=0.5);
	}
}

module finger(r_finger=2, h_finger=5, r_leaf=5) {
	// Finger structure
	color([205/255, 133/255, 63/255])
	resize([1.5*r_finger, 2*r_finger, h_finger]) 
	cylinder(r1=r_finger, r2=r_finger*0.5, h=h_finger, $fa=1, $fs=0.5);
	
	// Leaf of the finger
	color([0, 1, 0])
	translate([0, 0, h_finger*1.5]) 
	sphere(r=r_leaf, $fa=1, $fs=0.5);
}

module arm(r_arm=2, l_arm=15, a_shoulder=[0, 0, 0], a_elbow=[0, 0, 0], a_hand=[0, 0, 0]) {
	
	// Shoulder articulation
	rotate(a_shoulder) {
		
		// Connection between soulder and elbow
		color([205/255, 133/255, 63/255]) 
		rotate([-90, 0, 0]) 
		cylinder(r=r_arm, h=l_arm, $fa=1, $fs=0.5);
		
		translate([0, l_arm, 0]) {
			// Articulation point
			color([205/255, 133/255, 63/255]) 
			sphere(r_arm, $fa=1, $fs=0.5);
			
			rotate(a_elbow) { 
				// Connection between elbow and hand
				color([205/255, 133/255, 63/255]) 
				cylinder(r=r_arm, h=l_arm*0.6, $fa=1, $fs=0.5);
				
				translate([0, 0, l_arm*0.6]) 
				rotate(a_hand) {
					sphere(2, $fa=1, $fs=0.5);
					hand();
				}
			}
		}
	}
}

module leg(r_leg=6, a_leg=[0, 0, 0], a_foot=[0, 0, 0]) {
	rotate(a_leg) {
		// Leg
		resize([8, 5, 16]) {
			sphere(r_leg, $fa=1, $fs=0.5);
				
			translate([0, 0, -2*r_leg]) { 
				cylinder(r1=r_leg/4, r2=0.945*r_leg, h = 10, $fa=1, $fs=0.5);
				
				sphere(r=r_leg/4, $fa=1, $fs=0.5);
			}
		}
		// Foot
		translate([3.0, 0, -2*r_leg]) 
		rotate(a_foot) foot();
	}
}

module foot(r_leg=6) {
	resize([20, 6, 2])
	difference() {
		sphere(r_leg, $fa=1, $fs=0.5);
		translate([-r_leg, -r_leg, -2*r_leg]) cube(2*r_leg);
	}
}


translate([0, 4, 0]) 
scale([0.7, 0.7, 0.7]) 
arm(a_shoulder=[10,0, 0], a_elbow=[-20, 0, -10]);

translate([0, -3, 0])
scale([0.7, 0.7, 0.7]) 
mirror([0, 1, 0]) 
arm(a_shoulder=[-5,0, 0], a_elbow=[-20, 0, -15]);

trunk();

color([205/255, 133/255, 63/255]) translate([1,5,-22]) 
leg(a_leg=[15, 0, 0], a_foot=[-15, 0, 20]);

color([205/255, 133/255, 63/255]) translate([1,-2.5,-22])
leg(a_leg=[-15, 0, 0], a_foot=[15, 0, -15]);