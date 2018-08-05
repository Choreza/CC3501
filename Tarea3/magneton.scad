
module eye() {
	color([0.5, 0.5, 0.5])
	sphere(r=10, $fa=1, $fs=0.5);
	
	color([1, 1, 1])
	translate([4, 0, 0])
	resize([12, 16, 16])
	sphere(r=8, $fa=1, $fs=0.5);
	
	color([0, 0, 0])
	translate([9.8, 0, 0])
	resize([1, 4, 4])
	sphere(r=2, $fa=1, $fs=0.5);
}

module screw() {
	color([0.5, 0.5, 0.5])
	cylinder(r=1, h=5, $fa=1, $fs=0.5);
	
	color([0.5, 0.5, 0.5])
	difference() {
		translate([0, 0, 5])
		resize([8, 8, 3.5])
		sphere(r=4, $fa=1, $fs=0.5);
		
		translate([-4, -4, -3])
			cube(size=8);
	}
}

module magnet(a_magnet=[0, 0, -10]) {
	translate([-1.4, -4, 26.6])
	
	rotate(a_magnet + [0, 90, 0])
	scale([1.4, 1.4, 1.4]) {
		color([0.5, 0.5, 0.5])
		difference() {
			minkowski() {
			  cube([10, 6, 1.4]);
			  cylinder(r=2,h=1.4);
			}
			
			translate([-4,2.75,-0.1])
			minkowski() {
			  cube([12, 0.5, 1.8]);
			  cylinder(r=2,h=1.8);
			}
			
			translate([-1.9, -2, -0.1]) cube(size=3);
			translate([-1.9, 5, -0.1]) cube(size=3);
		}
		
		color([1, 0, 0])
		translate([0, -1.99, -0.01]) 
		cube(size=2.82);
		
		color([0, 0, 1])
		translate([0, 5.16, -0.01]) 
		cube(size=2.82);
	}
}

module head(a_magnet=[0, 0, -10]) {
	eye();
	
	// Screws
	
	translate([0, 0, 8]) 
	screw();
	
	rotate([0, 125, 35])
	translate([0, 0, 9]) 
	scale([0.7, 0.7, 0.7])
	screw();
	
	rotate([0, 125, -35])
	translate([0, 0, 9]) 
	scale([0.7, 0.7, 0.7])
	screw();
	
	// Magnet
	rotate([60, 0, 0])
	magnet(a_magnet);
	rotate([-60, 0, 0]) 
	magnet(a_magnet);
}


module magneton() {
	translate([0, 0, 13]) 
	head();
	
	rotate([120, 0, 0])
	translate([0, 0, 13]) 
	head(a_magnet=[0, 0, 10]);
	
	rotate([-120, 0, 0])
	translate([0, 0, 13]) 
	head(a_magnet=[0, 0, 10]);
	
}

magneton();

