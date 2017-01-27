/***************************************************************

Landing Gear
 - Writen by Eric Blackburn (ATMA)

 Landing Gear Manual
- lg_object - the main object that holds everything

  lg_object.apps
  lg_object.apps.load_app_by_name(name)
  lg_object.apps.load_app_by_appid(appid)
  lg_object.apps.

  lg_object.apps.app(name)
  lg_object.apps.app(name).id()
  lg_object.apps.app(name).title()
  lg_object.apps.app(name).body()
  lg_object.apps.app(name).settings_modal()
  lg_object.apps.app(name).icon()
  lg_object.apps.app(name).visible()
  lg_object.apps.app(name).loaded()
  lg_object.apps.app(name).loadapp()
  lg_object.apps.app(name).events()


  lg_object.apps.app(name).build_app // These commands are used to put together the invidual app object.
  lg_object.apps.app(name).build_app.
  lg_object.apps.app(name).compile_app


  lg_object.ajax
  lg_object.ajax.send(app, token, arguments)
  lg_object.ajax.event_read_queue(app, event, arguments)
  lg_object.ajax.event_write_queue(app, event, arguments)

  lg_object.access  - the main access commands and storage

  lg_object.access.request_auth_token()
  lg_object.access.auth_token()
  lg_object.access.login(auth token, user, pass)
  lg_object.access.logout()
  lg_object.access.user()
  lg_object.access.user.first_name()
  lg_object.access.user.last_name()
  lg_object.access.user.email()

  lg_object.cfg.cfg()

  lg_object.cfg.apps.cfg()
  lg_object.cfg.apps.app(name).cfg()
  lg_object.cfg.apps.app(name).from_server_to_local()
  lg_object.cfg.apps.app(name).from_local_to_server()

  lg_object.cfg.landing_gear.cfg()
  lg_object.cfg.landing_gear.from_server_to_local()
  lg_object.cfg.landing_gear.from_local_to_server()

  lg_object.cfg.golden.cfg()
  lg_object.cfg.golden.from_server_to_local()
  lg_object.cfg.golden.from_local_to_server()

  lg_object.golden.init()
  lg_object.golden.regComp()
  lg_object.golden.on()
  lg_object.golden.load_app(name)

  lg_object.local_storage.save()
  lg_object.local_storage.load()

  lg_object.gui
  lg_object.gui.menu.act.button.animation
  lg_object.gui.menu.act.button.animation.start
  lg_object.gui.menu.act.button.animation.stop
  lg_object.gui.menu.act.button.animation.toggle
  lg_object.gui.menu.act.button.animation.speed
  lg_object.gui.menu.act.button.animation.replay_pause
  lg_object.gui.menu.act.button.animation.playing

  lg_object.gui.menu.act.button.animation.type
  lg_object.gui.menu.act.button.animation.type.jiggle
  lg_object.gui.menu.act.button.animation.type.flash
  lg_object.gui.menu.act.button.animation.type.shake
  lg_object.gui.menu.act.button.animation.type.pulse
  lg_object.gui.menu.act.button.animation.type.tada
  lg_object.gui.menu.act.button.animation.type.bonce

  lg_object.gui.menu.act.button.badge
  lg_object.gui.menu.act.button.badge.on
  lg_object.gui.menu.act.button.badge.off
  lg_object.gui.menu.act.button.badge.toggle
  lg_object.gui.menu.act.button.badge.value

  lg_object.gui.menu.act.button.alerts
  lg_object.gui.menu.act.button.alerts.count
  lg_object.gui.menu.act.button.alerts.sound

  lg_object.gui.menu.act.button.visible
  lg_object.gui.menu.act.button.visible.toggle

  lg_object.gui.menu.act.button.enabled

  lg_object.gui.menu.act.button.direction
  lg_object.gui.menu.act.button.direction.top
  lg_object.gui.menu.act.button.direction.left
  lg_object.gui.menu.act.button.direction.right
  lg_object.gui.menu.act.button.direction.bottom

  lg_object.gui.menu.body
  lg_object.gui.menu.body.animation
  lg_object.gui.menu.body.animation.type
  lg_object.gui.menu.body.animation.type.overlay
  lg_object.gui.menu.body.animation.type.push
  lg_object.gui.menu.body.animation.type.scale
  lg_object.gui.menu.body.animation.type.uncover
  lg_object.gui.menu.body.animation.type.slide_along
  lg_object.gui.menu.body.animation.type.slide_out


  lg_object.gui.menu.body.menu_button
  lg_object.gui.menu.body.menu_button.icon_type
  lg_object.gui.menu.body.menu_button.icon_html
  lg_object.gui.menu.body.menu_button.visible
  lg_object.gui.menu.body.menu_button.link

  lg_object.gui.menu.body.home
  lg_object.gui.menu.body.home.icon_type
  lg_object.gui.menu.body.home.icon_html
  lg_object.gui.menu.body.home.visible
  lg_object.gui.menu.body.home.link

  lg_object.gui.menu.body.settings
  lg_object.gui.menu.body.settings.icon_type
  lg_object.gui.menu.body.settings.icon_html
  lg_object.gui.menu.body.settings.visible
  lg_object.gui.menu.body.settings.link

  lg_object.gui.menu.body.search
  lg_object.gui.menu.body.search.icon_type
  lg_object.gui.menu.body.search.icon_html
  lg_object.gui.menu.body.search.visible
  lg_object.gui.menu.body.search.link

  lg_object.gui.menu.body.favapps
  lg_object.gui.menu.body.favapps.icon_type
  lg_object.gui.menu.body.favapps.icon_html
  lg_object.gui.menu.body.favapps.visible
  lg_object.gui.menu.body.favapps.link

  lg_object.gui.menu.body.device
  lg_object.gui.menu.body.device.icon_type
  lg_object.gui.menu.body.device.icon_html
  lg_object.gui.menu.body.device.visible
  lg_object.gui.menu.body.device.link

  lg_object.gui.menu.body.signin
  lg_object.gui.menu.body.signin.icon_type
  lg_object.gui.menu.body.signin.icon_html
  lg_object.gui.menu.body.signin.visible
  lg_object.gui.menu.body.signin.link

  lg_object.gui.menu.body.account
  lg_object.gui.menu.body.account.icon_type
  lg_object.gui.menu.body.account.icon_html
  lg_object.gui.menu.body.account.visible
  lg_object.gui.menu.body.account.link

  lg_object.gui.menu.body.dashboard
  lg_object.gui.menu.body.dashboard.icon_type
  lg_object.gui.menu.body.dashboard.icon_html
  lg_object.gui.menu.body.dashboard.visible
  lg_object.gui.menu.body.dashboard.link

  lg_object.gui.menu.body.signout
  lg_object.gui.menu.body.signout.icon_type
  lg_object.gui.menu.body.signout.icon_html
  lg_object.gui.menu.body.signout.visible
  lg_object.gui.menu.body.signout.link

  lg_object.gui.body.


  lg_object.gui.modals.



  lg_object.main


 - ajax
- - cfg
- - gold
- - local_storage
- - gui
- - main




****************************************************************/


var App_Ajax_Pipe = function () {


};

var app_object = function () {
	this.name = ""; // string the literal name of the app and used as a way to identify it
	this.uid = ""; // string the unique id name of the app and used as another way to identify it

	this.active = false; // bool if the is open on the users active on the devices landing gear page

	this.auth_token = "";// string the token given to this app from the server to allow users to make their next ajax and rest calls
	this.auth_token_expire = ""; // string the time when the token expires.

	this.config = {};//json the public config info saved in the object to store data

	this.css  = [];      //list the css files to apply to the header
	this.font = [];      //list fibt fukes
	this.images = [];    //list images
	this.js_files = [];  //list
	this.templates = []; // list names of the theme names

	this.index = ""; //
	this.settings = {}; //
	this.menu = ""; //

	this.title = "";// string, change tab header string or return it

	this.icon_html = "";// string, change string to or return  it
	this.body_html = ""; // string, return or set the body html
	this.menu_html = "";// string, return or set menu html
	this.settings_html = ""; // string, retrn or set modal settings html

	this.events = {}; // events regisutered with this ap
	this.alerts = {}; // new active alerts

	this.ajax_conduit = new App_Ajax_Pipe();
};

var lg_apps_array_object = function () {
	this.apps_array = {};

	this.app = {};

	//this.add_app

	// consturctor

	//destructor

};

var lg_gold_object = function () {


}

var lg_ajax = function () {

};

var lg_object = function () {
	/*
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
	this.access_token = "";

	//lg_device: new lg_device_object(),

	this.lg_apps = lg_apps_array_object();

	this.set_accesss_token = function (token) {

		this.access_token = token;
	};

	this.login(user, pass, token) = function () {


	};


};




//<<<<<<< HEAD
//lg_object.init();  // initialize our object and virtual dom

// if the user is logged in they get their saved config
// if the user is logged out they get the default config
// try and check if the user is new or returning,
//   if they are a returner try and identify them.

//lg_object.cfg.landing_cfg.from_server_to_local();  // downloads the landing gear config from the server to the local storage.
//lg_object.cfg.landing_cfg.from_local_to_server();  // uploads the landing gear config to the server.
//lg_object.cfg.golden_cfg.from_server_to_local();  // downloads golden layout config to the local web storage.
//lg_object.cfg.golden_cfg.from_local_to_server();  // uploads golden layout config to the web storage.

//lg_object.main.gui.load_apps_into_virtual_dom();  // downloads and loads the apps from the landing gear config into the dom.

//lg_object.main.body.load_template(name);  // this is the main body template colors.
//lg_object.main.body.save_template(name); // save the current template with the name.
//lg_object.main.body.


//lg_object.main.login(user, pass, token);

//if (lg_object.logged() === True) {
//	lg_object.gold.config();
//	lg_object.menu_button.animation_type();
//	lg_object.menu_button.animate_start();
//	lg_object.menu.populate_fav_menu();
//	lg_object.device.set();
//


//	//lg_object.apps.load('appname or appid');  loads the name of the app into our js virtual dom
//	//lg_object.app['appname'].cmd(); // our style structure



/*
=======
//lg_object.init();
lg_object.set_access_token();
lg_object.login(user, pass, token);

if (lg_object.logged() === True) {
	lg_object.gold.user_config(); // lets query and get the user's golden layout config for where the apps go on the screen.
	//lg_object
	lg_object.menu_button.animation_type(); // lets query and get the users animation type
	//lg_object.menu_button.animate_start();
	lg_object.menu.populate_fav_menu();
	lg_object.device.detect_device();
	lg_object.events.alert('succecss');
>>>>>>> origin/master
}
*/



