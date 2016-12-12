/*
 * landing_gear.js is the primary loading system and holds all landing gear glue code.
 * 
 * javascript UI control system
 * - menu button
 * - - animate
 * - - alerts
 * - - badges
 * - device 
 * - fav apps
 * - my default home page 
 * - signed in
 * - active apps
 * - - app id
 * - - app name
 * - - app body
 * - - app settings modal
 * - - app icon
 * - - app visisbility
 * -
 *
 */
 
 
 
 
var menu_button_object =  function () {
	
	//private variables
	// a jquery object that is the menu.
	this.menu_pointer_obj = $('.lg_menubutton'); // default menu button to point at
	
	// menu pointer interval object
	this.menu_interval_obj = null;
	
	// true/false if the animation is playing or not.
	this.animation_on_bool = false;
	
	// interval, in milliseconds length of time it takes to complete an animation cycle.
	this.animation_speed_obj = 1000;
	
	// interval, in milliseconds length of time it takes between animiation cycles.
	this.animation_pause_obj = 2000;
	
	// string, name of animation types.
	this.animation_type_obj = "bounce";
	
	// true/false if the badge is on or off.
	this.badge_on_bool = false;
	
	// is a string or interger.
	this.badge_value = '';
	
	// construction auto loads.
	//alert("a");
	
	//class functions.
	
	this.menu_pointer = function(jqueryobj) {
		this.menu_pointer_obj = jqueryobj;
	};
	
	// begin playing a constant animation set by animation_type.
	this.animation_start = function () {
		if (this.animation_on_bool == false) {
			
			this.animation_on_bool = true;
			var speed = this.animation_speed_obj+'ms';
			
			if (this.animation_type_obj == "jiggle") {
				
				this.menu_interval_obj = setInterval (
					function() {
						$('.lg_menubutton').transition("jiggle", speed);
					},
					this.animation_pause_obj
				);
			}
			else if (this.animation_type_obj == "flash") {
				
				this.menu_interval_obj = setInterval (
					function() {
						$('.lg_menubutton').transition("flash", speed);
					},
					this.animation_pause_obj
				);
			}
			else if (this.animation_type_obj == "shake") {
				
				this.menu_interval_obj = setInterval (
					function() {
						$('.lg_menubutton').transition("shake", speed);
					},
					this.animation_pause_obj
				);
			}
			else if (this.animation_type_obj == "pulse") {
				
				this.menu_interval_obj = setInterval (
					function() {
						$('.lg_menubutton').transition("pulse", speed);
					},
					this.animation_pause_obj
				);
			}
			else if (this.animation_type_obj == "tada") {
				
				this.menu_interval_obj = setInterval (
					function() {
						$('.lg_menubutton').transition("tada", speed);
					},
					this.animation_pause_obj
				);
			}
			else if (this.animation_type_obj == "bounce") {
				
				this.menu_interval_obj = setInterval (
					function() {
						$('.lg_menubutton').transition("bounce", speed);
					},
					this.animation_pause_obj
				);
			}
			else {
				return false;
			}
			
			return true;
		}
		else {
			return false;
		}
	
	};
	
	// end playing a constant animation.
	this.animation_stop = function () {
		if (this.animation_on_bool == true) {
			//clear the interval timre loop
			clearInterval(this.menu_interval_obj);
			
			//set the object as no longer on.
			this.animation_on_bool = false;
			
			//actually clear the animations from the sematnic transitions.
			$('.lg_menubutton').transition('stop all').transition('clear queue');
			
			// return success
			return true;
		}
		else {
			// failed to terminate any object.
			return false;
		}
	};
	
	// automatically start or stop playing the animation
	this.animation_toggle = function () {
		if (this.animation_on_bool == true) {
			this.animation_stop();
		}
		else {
			this.animation_start();
		}
	};
	
	// set or retrieve the speed the animation plays at returns true on successful set, false on failure
	this.animation_speed = function (time) {
		if (time == null) {
			return this.animation_speed_obj;
		}
		else {
			try {
				this.animation_speed_obj = time;
				return true;
			}
			catch (err) {
				return false;
			}
			
		}
	};
    
    
    
	
	// return or set the time it pauses between animation sequences
	this.animation_pausetime = function (time) {
		//alert(time);
		if (time == null) {
			return this.animation_pause_obj;
		}
		else {
			try {
				this.animation_pause_obj = time;
				return true;
			}
			catch (err) {
				return false, err;
			}
			
		}
	};
	
	// set or return the name of the animation playing
	this.animation_type = function (name) {
		if (name == null) {
			return this.animation_type_obj;
		}
		else {
			try {
				switch (name) {
					case "jiggle":
						this.animation_type_obj = name;
						return ture;
					case "flash":
						this.animation_type_obj = name;
						return true;
					case "shake":
						this.animation_type_obj = name;
						return true;
					case "pulse":
						this.animation_type_obj = name;
						return true;
					case "tada":
						this.animation_type_obj = name;
						return true;
					case "bounce":
						this.animation_type_obj = name;
						return true;
					default:
						break;
				}
				return false;
			}
			catch (err) {
				return false, err
			}
		}
	};
	
	// returns if the animation is currently playing or not.
	this.animation_playing = function () {
		return this.animation_on_bool;
	};
	
	// Future features.
	// turn on a badge
	this.badge_on = function () { // applies a bootstrap type badges to the icon
		
	};
	
	// turn off the badge
	this.badge_off = function () {
		
	};
	
	//set or return the badge value.
	this.badge_value = function (value) {
		//alert(value);
	};

};


// control menu mechanics of the pusher shit
var menu_body_object = function () {
	this.bar_slide_direction = "top";
	this.bar_push_animation_obj = "push";
	//this.bar
};

// controls what appears in the favoriate apps dropdown bar
var menu_favapps_object = function () {
	
};

// possible future feature of extra programmable app buttons that apear next to the other items.
var menu_appsbar_object = function () {
	
};

// this is where we store device spcific data 
var lg_device_object = function () {
	
};

var lg_apps_object = function () {
	this.goldy = "";
	
	this.gold_config_json = ""; // golden layout config json
	this.gold_config_md5_integerity_key = ""; // md5 key of json to check intergity
	this.gold_config_md5_integerity_bool = false; // if it checks out.
	
	this.gold_golden_object = null;
	this.gold_golden_container = "#contents";
	
	this.app_golden_components = [];
	
	this.apps_containers_list = []; // stores an array of the apps 
	
	var parent = this;
	
	/// golden layout functions
	this.gold = {
		/*
		lg_object.lg_apps.gold.goldcmd1().goldcmd2().ectcmd();
		gold.config // JSON, save or return new config data
		gold.container_location // string pointing to the object where we want to stick our goldenlayout
		gold.golden_obj // golden layout object, save or return it
		gold.register_component // save or read a golden layoput component in our landing gear system.\
		gold.app_window_container
		gold.events // our events system
		*/
		
		config: function (config) {
			if (config === undefined) {
				return parent.gold_config_json;
			}
			else {
				try {
					parent.gold_config_json = config;
					return true;
				}
				catch (err) {
					return false, err;
				}
			}
			return false;
		},
		
		container_location: function(location) {
			if (location === undefined) {
				return parent.gold_golden_container;
			}
			else {
				try {
					parent.gold_golden_container = location;
					return true;
				}
				catch (err) {
					return false, err;
				}
			}
			return false;
		},
		
		golden_obj_generate: function () {
			try {
				parent.gold_golden_object = new GoldenLayout(parent.gold_config_json, parent.gold_golden_container);
				return true;
			}
			catch (err) {
				return false, err;
			}
		},
		golden_obj: function () {
			try { return parent.gold_golden_object; }
			catch (err) {
				return false, err;
			}
		},
		
		register_component: function (component_name, component_state) {
			try {
				parent.gold_golden_object.registerComponent(component_name, component_state);
				return true;
			}
			catch (err) {
				return flase, err;
			}
		},
		
		events: function () {
		
		}
	};
	
	this.app_name = ""; // string the literal name of the app and used as a way to identify it
	this.app_uid = ""; // string the unique id name of the app and used as another way to identify it
	this.app_active = false; // bool if the is open on the users active on the devices landing gear page
	this.app_auth_token = "";// string the token given to this app from the server to allow users to make their next ajax and rest calls
	this.app_auth_token_expire = ""; // string the time when the token expires.
	this.app_config = "";//json the public config info saved in the object to store data 
	this.app_css  = [];      //list the css files to apply to the header
	this.app_font = [];      //list fibt fukes
	this.app_images = [];    //list images 
	this.app_js_files = [];  //list
	this.app_templates = []; // list names of the theme names
	this.app_index = ""; // 
	this.app_settings = "";// 
	this.app_menu = ""; // 
	this.app_icon_html = "";// string, change string to or return  it
	this.app_title = "";// string, change tab header string or return it
	this.app_body_html = ""; // string, return or set the body html
	this.app_menu_html = "";// string, return or set menu html
	this.app_settings_html = ""; // string, retrn or set modal settings html
	this.app_events = ""; // events regisutered with this ap
	this.app_alerts = "";// new actuive alerts
	
	this.app = {
		/*
		main controls:
			command structure concept examples:
			lg_object.lg_apps.app.name['appname'].appcmd().appcmd();
			lg_object.lg_apps.app.id['43212dadf3'].appcmd();
			lg_object.lg_apps.app.etc

			app.name // string the literal name of the app and used as a way to identify it
			app.uid  // string the unique id name of the app and used as another way to identify it
			app.active // bool if the is open on the users active on the devices landing gear page
			app.auth_token  // string the token given to this app from the server to allow users to make their next ajax and rest calls
			app.auth_token_expire // string the time when the token expires.

			app.config //json the public config info saved in the object to store data 
			app.css    //list the css files to apply to the header
			app.font   //list fibt fukes
			app.images //list images 
			app.js_files //list
			app.templates // list names of the theme names

			app.index // 
			app.settings // 
			app.menu // 

			app.icon_html // string, change string to or return  it
			app.title // string, change tab header string or return it
			app.body_html // string, return or set the body html
			app.menu_html // string, return or set menu html
			app.settings_html // string, retrn or set modal settings html

			app.events // events regisutered with this ap
			app.alerts // new actuive alerts
		*/
		name: function (name) {
			if (name === undefined) {
				return parent.app_name;
			}
			else {
				try {
					parent.app_name = name;
					return true;
				}
				catch (err) {
					return flase, err;
				}
			}
		},
		
		uid: function (uid) {
			if (name === undefined) {
				return parent.app_uid;
			}
			else {
				try {
					parent.app_uid = uid;
					return true;
				}
				catch (err) {
					return flase, err;
				}
			}
		},
		
		active: function (activity) {
			if (activity === undefined) {
				return parent.app_active;
			}
			else {
				try {
					return parent.app_active;
				}
				catch (err) {
					return flase, err;
				}
			}
		},
		
		auth_token: function (token) {
			if (token === undefined) {
				return parent.app_auth_token;
			}
			else {
				try {
					return parent.app_auth_token;
				}
				catch (err) {
					return flase, err;
				}
			}
		},
		
		auth_token_expire: function (expiration) {
			if (expiration === undefined) {
				return parent.app_auth_token_expire;
			}
			else {
				try {
					return parent.app_auth_token_expire;
				}
				catch (err) {
					return flase, err;
				}
			}
		},
		
		config: function (config) {
			if (config === undefined) {
				return parent.app_config;
			}
			else {
				try {
					return parent.app_config;
				}
				catch (err) {
					return flase, err;
				}
			}
		},
		
		css: function () {
			
		},
		
		font: function () {
			
		},
		
		image: function () {
			
		},
		
		js_files: function () {
			
		},
		
		templates: function () {
			
		},
		
		index: function () {
			
		},
		
		settings: function () {
			
		},
		
		menu: function () {
			
		},
		
		icon_html: function () {
			
		},
		
		title: function () {
			
		},
		
		body_html: function () {
			
		},
		
		menu_html: function () {
			
		},
		
		settings_html: function () {
			
		},
		
		events: function () {
			
		},
		
		alerts: function () {
			
		}
		
	};
	
	this.call = {
	/*
	 server side ajax and other calls 
	  
	*/
		
		
	}
	
	/* initalize components and all that shit */
	// first ajax call to get our page layout config
	//ajax()
	
};
var lg_object =  {
	
	menu_button: new menu_button_object(),
	menu_body: new menu_body_object(),
	menu_favapps: new menu_favapps_object(),
	menu_appsbar: new menu_appsbar_object(),
	
	/*
	lg_signin:
	lg_signout:
	lg_register:
	lg_lostpass:
	*/
	
	lg_device: new lg_device_object(),
	apps: new lg_apps_object()
	
};


console.log(lg_object.apps.gold.config("asdfad")); // put in our golden layout json config.
console.log(lg_object.apps.gold.container_location("#contents")); // container element id 
console.log(lg_object.apps.gold.container_location()); // container element id 
console.log(lg_object.apps.gold.golden_obj_generate()); // lets generate and store the goldenlayout object
console.log(lg_object.apps.gold.golden_obj()); // now return our golden layout object to od whateves
console.log(lg_object.apps.gold.register_component('lg_weather'));


//console.log(lg_object.apps.gold.config("asdfad"));
//console.log(lg_object.apps.gold.golden_obj());
//lg_object.apps.gold.golden_obj_generate();
//console.log(lg_object.apps.gold.golden_obj());

//var lg_control = new landing_gear_system();
$(document).ready(function() {
	//var lg_control = lg_object();
	
	//lg_object.menu_button.animation_type('bounce');
	//lg_object.menu_button.animation_speed(2000);
	//lg_object.menu_button.animation_start();
	//setTimeout((function () { lg_object.menu_button.animation_stop(); alert("aa"); }), 10000);
	//
	//console.log(lg_object.apps.gold.config());
	//lg_object.lg_apps.gold.config();
	
	//test.menu_button.animate_start();
	
	$('.ui.sidebar.lg_menu_body').sidebar('setting', 'transition', 'overlay');
	
	$('.lg_menubutton').click(function() {
		//alert("asdf");
		$('.ui.sidebar.lg_menu_body').sidebar('toggle');
		
	});
	
	$('.modals_login').modal({
		blurring  : true,
		transition: 'vertical flip',
		//onHide    : function () {
			//alert("wasdf");
		//	alert("aborting");
		//	modal_login_postlink.abort();
			
			//return true;
		//}
		//closable  : false,
		//onDeny    : function () {
		//	alert('Please wait while we get your data!');
		//	return false;
		//}
	});
	//'setting', 'transition', 'vertical flip');
	
	
	/*buttons to click
	 */
	$('.button_modal_homescreen').click(function() {
		//$('.modals_settings').modal('show');
	});
	$('.button_modal_settings').click(function() {
		$('.modals_settings').modal('show');
	});
	$('.button_modal_searchapps').click(function() {
		//$('.modals_settings').modal('show');
	});
	$('.button_modal_favapps').click(function() {
		//$('.modals_settings').modal('show');
	});


	$('.button_menu_modal_login').click(function() {
		$('.modals_login').modal('show');
	});
	

	//$('.lg_landinggear_menu').dropdown();
	$('.lg_menuicon_homescreen').popup();
	$('.lg_menuicon_settings').popup();
	$('.lg_menuicon_search').popup();
	$('.lg_menuicon_fav').popup();
	$('.lg_menuicon_login').popup();
	$('.lg_menuicon_settings').popup();
	$('.lg_menuicon_dash').popup();
	$('.lg_menuicon_logout').popup();
	
	/*
	setInterval (
		function() {
			$('.lg_menubutton').transition('bounce', '1000ms');
		},
		2000
	);
	*/ 
	
	$('.ui.dropdown').dropdown();
	
	$('.button_menu_logout').click(function() {
		$('.modals_logout').modal('show');
	});
	
	$('.button_modal_logout_yes').click(function() {
		//alert("asdf");
		document.location = "?p=logout";
	});
	
	
	$('.modals_registeruser').modal('attach events', '.modals_login .button_local_register');
	$('.modals_login').modal('attach events', '.modals_registeruser .button_modal_register_cancel');
	
	//lg_object.menu_button.animation_toggle();
	//lg_object.menu_button.animation_pausetime(100);
	//setTimeout(function () { lg_object.menu_button.animation_toggle() } , 6000);
	
	//alert();
	//setTimeout(lg_object.menu_button.animation_stop(), 10000);
	
	/*
	menu_interval_obj = setInterval (
		function() {
			$('.lg_menubutton').transition("bounce", speed);
		},
		this.animation_pause_obj
	);*/
	//$('.lg_menubutton').transition("bounce", 2000).transition('set looping');
	
});
