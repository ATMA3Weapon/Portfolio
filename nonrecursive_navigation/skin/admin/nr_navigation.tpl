<div id="general" class="tab_content">
  <h3>{$MODULE_LANG.page_view_stats}</h3>
  
  {if $STATS}
    <p>{$MODULE_LANG.page_view_stats_desc}</p>
    <table class="list">
    	<thead>
    		<tr>
    			<td>{$MODULE_LANG.visitor_id}</td>
    			<td>{$MODULE_LANG.ip_address}</td>
				<td>{$MODULE_LANG.browser}</td>
				<td>{$MODULE_LANG.first_visit}</td>
				<td>{$MODULE_LANG.last_visit}</td>
				<td>{$MODULE_LANG.page_views}</td>
    		</tr>
    	</thead>
    	<tbody>
    		{foreach from=$STATS item=STAT}
    		<tr>
    			<td>{$STAT.id}</td>
    			<td>{$STAT.ip_address}</td>
				<td>{$STAT.browser}</td>
				<td>{$STAT.first_visit}</td>
				<td>{$STAT.last_visit}</td>
				<td>{$STAT.page_views}</td>
    		</tr>
    		{/foreach}
    	</tbody>
    </table>
  {else}
    <p>{$MODULE_LANG.no_stats}</p>
  {/if}
</div>