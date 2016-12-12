/********************************
* Class StockDataRequest
********************************/
StockDataRequest = function( tickerSymbol, callback ) {
    this._tickerSymbol = tickerSymbol;
    this._callback = callback;
    this._loadData();
};

StockDataRequest.prototype._createYqlQuery = function() {
    var url =   'https://query.yahooapis.com/v1/public/yql?' +
                'q=select * from yahoo.finance.historicaldata '+
                'where symbol = "' + this._tickerSymbol + '" ' +
                'and startDate = "2013-09-11" and endDate = "2014-03-10"&' + 
                'format=json&diagnostics=true&' +
                'env=store://datatables.org/alltableswithkeys';

    return encodeURI( url );
};

StockDataRequest.prototype._loadData = function() {
    $.ajax({
        url: this._createYqlQuery( this._tickerSymbol ),
        success: this._onDataReceived.bind( this ),
        cache: true,
        dataType: 'jsonp'
    });
};

StockDataRequest.prototype._onDataReceived = function( rawData ) {
    var highchartsData = this._transformDataForHighCharts( rawData );
    this._callback( highchartsData );
};

StockDataRequest.prototype._transformDataForHighCharts = function( rawData ) {
    var quotes = rawData.query.results.quote,
        data = [],
        i;

    for( i = quotes.length - 1; i >=0; i-- ) {
        data.push([
            ( new Date( quotes[ i ].Date ) ).getTime(),
            parseFloat( quotes[ i ].Open )
        ]);
    }

    return data;
};

/********************************
* Class StockChartComponent
********************************/
StockChartComponent = function( container, state ) {

    this._highChartsConfig = {
        title: { text: 'Historic prices for ' + state.companyName },
        series: [],
        plotOptions: { line: { marker: { enabled: false } } },
        xAxis:{ type: 'datetime' },
        yAxis:{ title: 'Price in USD' },
        chart:{
            renderTo: container.getElement()[ 0 ]
        }
    };

    this._chart = null;
    this._container = container;
    this._container.setTitle( 'Chart for ' + state.companyName );
    this._state = state;
    this._container.on( 'open', this._createChart.bind( this ) );
};

StockChartComponent.prototype._createChart = function() {
    this._chart = new Highcharts.Chart( this._highChartsConfig );
    this._chart.showLoading( 'Loading data...' );
    new StockDataRequest( this._state.tickerSymbol, this._onDataReady.bind( this ) );
};

StockChartComponent.prototype._onDataReady = function( highchartsData ) {
    this._chart.addSeries({
        color: this._state.color,
        name: this._state.companyName,
        data: highchartsData
    });

    this._chart.hideLoading();
    this._bindContainerEvents();
};

StockChartComponent.prototype._bindContainerEvents = function() {
    this._container.on( 'resize', this._setSize.bind( this ) );
    this._container.on( 'destroy', this._chart.destroy.bind( this._chart ) );
};

StockChartComponent.prototype._setSize = function() {
    this._chart.setSize( this._container.width, this._container.height );
};

/********************************
* Build Welcome To Landing Gear
********************************/
WelcomeToLandingGearComponent_Main = function( container, state ) {
	container.setTitle("Welcome To Landing Gear");
	container.getElement().html( '<h2>Welcome to Landing Gear ' + state.user_name + '</h2><br /><br />');
}
WelcomeToLandingGearComponent_Settings = function( container, state ) {
	container.setTitle("Welcome To Landing Gear Settings");
	container.getElement().html( '<h2>Welcome to Landing Gear Settings' + state.user_name + '</h2>New User Name: <input name="newusername" id="newusername" value="'+state.user_name+'" />');
}
RSSReaderComponent_Main = function(container, state) {
	container.setTitle("Google RSS FEED");
	container.getElement().html('AJAX FEED IN');
}

WeatherToLandingGearComponent = function(container, state) {
	container.setTitle("Weather Gear");
	container.getElement().html('<i class="wi wi-day-sunny"></i> ' + state.test + ' ...fff');
		
}

/********************************
* Initialise Layout
********************************/
$(function(){
	
	

	var config = {
   "settings":{
      "hasHeaders":true,
      "constrainDragToContainer":true,
      "reorderEnabled":true,
      "selectionEnabled":false,
      "popoutWholeStack":false,
      "blockedPopoutsThrowError":true,
      "closePopoutsOnUnload":true,
      "showPopoutIcon":false,
      "showMaximiseIcon":false,
      "showCloseIcon":true
   },
   "dimensions":{
      "borderWidth":5,
      "minItemHeight":10,
      "minItemWidth":10,
      "headerHeight":20,
      "dragProxyWidth":300,
      "dragProxyHeight":200
   },
   "labels":{
      "close":"close",
      "maximise":"maximise",
      "minimise":"minimise",
      "popout":"open in new window",
      "popin":"pop in"
   },
   "content":[
      {
         "type":"column",
         "isClosable":true,
         "reorderEnabled":true,
         "title":"",
         "content":[
            {
               "type":"row",
               "isClosable":true,
               "reorderEnabled":true,
               "title":"",
               "height":100,
               "content":[
                  {
                     "type":"stack",
                     "isClosable":true,
                     "reorderEnabled":true,
                     "title":"",
                     "activeItemIndex":0,
                     "width":16.553524804177545,
                     "content":[
                        {
                           "type":"component",
                           "componentName":"WeatherToLandingGearComponent",
                           "componentState":{
                              "test":"test"
                           },
                           "isClosable":true,
                           "reorderEnabled":true,
                           "title":"Weather Gear"
                        }
                     ]
                  },
                  {
                     "type":"stack",
                     "height":100,
                     "isClosable":true,
                     "reorderEnabled":true,
                     "title":"",
                     "activeItemIndex":0,
                     "width":83.44647519582246,
                     "content":[
                        {
                           "type":"component",
                           "componentName":"WelcomeToLandingGear_Main",
                           "componentState":{
                              "user_name":"Eric"
                           },
                           "isClosable":true,
                           "reorderEnabled":true,
                           "title":"Welcome To Landing Gear"
                        }
                     ]
                  }
               ]
            }
         ]
      }
   ],
   "isClosable":true,
   "reorderEnabled":true,
   "title":"",
   "openPopouts":[

   ],
   "maximisedItemId":null
}
	

	var myLayout = new GoldenLayout(config, "#contents");
	


	//console.dir(myLayout);

	//myLayout.registerComponent( 'stockChart', StockChartComponent );
	
	myLayout.registerComponent('WelcomeToLandingGear_Main', WelcomeToLandingGearComponent_Main);
	myLayout.registerComponent('WelcomeToLandingGear_Settings', WelcomeToLandingGearComponent_Settings);
	myLayout.registerComponent('WeatherToLandingGearComponent', WeatherToLandingGearComponent);
	
	//myLayout.updateSize(1250, 100);
	
	
	
	//myLayout.on( 'stateChanged', function(container, state){
		//var state = JSON.stringify(myLayout.toConfig());
		//console.log("change "+ myLayout + " : "+ container + " : " +state);
		//console.log(state);
		//localStorage.setItem( 'savedState', state );
	
	//});
	
	myLayout.on( 'stackCreated', function( stack ){
			
		//HTML for the templates stuffs
		var templates_settings = $($('template.lg_header_settings').html());
		
		//console.log(var_dump(templates_close));
		
		// settings button
		var settingsBtn = templates_settings.find('.lg_header_settings_button');
		
		//show settings button
		
		
		// Add the colorDropdown to the header
		stack.header.controlsContainer.prepend(templates_settings);
	});
	
	
	myLayout.init();
	//lg_top_body_row
	
	
	var menu_row_container = $(".lg_menu_row");
	var body_row_container = $(".lg_body_row");
	
	var menu_slider_container = $(".lg_menuslider");
	
	// the viewport is the area where goldenlayout takes place.
	var viewport_height = $(window).height() - menu_row_container.height() - 2;
	
	// set the viewport width and height and update goldenlayout to adjust its size to fit the viewport.
	body_row_container.height(viewport_height);
	myLayout.updateSize(menu_row_container.width(), viewport_height);
	
	
	//create an event to check if menu has slid out and we then adjust the height/width of everything to fit.
	//menu_slider_container.on('webkitTransitionEnd', function() { 
		
		
	//});
	
	//var menuslidebar_container = document.getElementById('lg_slidemenubar');
	//resizing sensor for the body and menu adjustments
	//new ResizeSensor(menuslidebar_container, function() {
	//	console.log("a");
	//	alert("a");
	//	// 
	//	//var viewport_new_height = $(window).height() - menu_row_container.height();
	//	//var viewport_new_width  = $
	//});
	
	
	
	//var menu_container = document.getElementById('menu');
	
	//var newheight = $(window).height() - menu_container.offsetHeight;
	//$('.contents').height(newheight);
	//myLayout.updateSize(newheight);
	
	//new ResizeSensor(menu_container, function() {
	//	var newheight = $(window).height() - menu_container.offsetHeight;
	//	$('.contents').height(newheight);
	//	myLayout.updateSize(menu_container.offsetWidth, newheight);
	//});

	//var main_container = document.getElementById('contents');
	//new ResizeSensor(main_container, function() {
	//	var newheight = $(window).height() - menu_container.offsetHeight;
	//
	//});

});
    


"5": {"LinkURL": "mygold.js"},

