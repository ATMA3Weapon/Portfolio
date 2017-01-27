<form action="{$VAL_SELF}" method="post" enctype="multipart/form-data">
  <div id="visitor_stats" class="tab_content">
	<h3>{$LANG.visitor_stats.module_title}</h3>
	<p>{$LANG.visitor_stats.module_description}</h3></p>
	<fieldset><legend>{$LANG.module.config_settings}</legend>
	  <div><label for="status">{$LANG.common.status}</label><span><input type="hidden" name="module[status]" id="status" class="toggle" value="{$MODULE.status}" />&nbsp;</span></div>
	  <div><label for="text_color">{$LANG.visitor_stats.text_color}</label><span><input name="module[text_color]" id="text_color" class="textbox" type="text" value="{$MODULE.text_color}" /></span></div>
	  <div><label for="border_color">{$LANG.visitor_stats.border_color}</label><span><input name="module[border_color]" id="border_color" class="textbox" type="text" value="{$MODULE.border_color}" /></span></div>
	  <div><label for="background_color">{$LANG.visitor_stats.background_color}</label><span><input name="module[background_color]" id="background_color" class="textbox" type="text" value="{$MODULE.background_color}" /></span></div>
	  <div>
		<label for="font_family">{$LANG.visitor_stats.font_family}</label>
		<span>
		  <select name="module[font_family]">
      		<option value="Georgia" {$SELECT_font_family_Georgia}>Georgia</option>
      		<option value="Arial" {$SELECT_font_family_Arial}>Arial</option>
    	  </select>
		</span>
	  </div>
	 </fieldset>
	 <fieldset><legend>{$LANG.visitor_stats.preview}</legend>
	  <div>
		{$COUNTER_PREVIEW}	
	  </div>
	</fieldset>
	<p>The text &quot;{$LANG.visitor_stats.page_views}&quot; can be changed <a href="?_g=settings&node=language&language=en-US&type=modules%2Fplugins%2Fvisitor_stats%2Flanguage%2Fmodule.definitions.xml">here</a>.</p>
	<p>To show the above counter on your store front the macro <strong>{literal}{$VISITOR_STATS_COUNTER}{/literal}</strong> needs to be added anywhere in your main.php template file. 
  </div>
  {$MODULE_ZONES}
  <div class="form_control">
	<input type="submit" name="save" value="{$LANG.common.save}" />
  </div>
  <input type="hidden" name="token" value="{$SESSION_TOKEN}" />
</form>