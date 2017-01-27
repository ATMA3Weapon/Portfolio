<li {if isset($BRANCH.children)}class="dropdown-submenu drp-nav"{/if}>
	<a href="{$BRANCH.url}" title="{$BRANCH.name}">
		{$BRANCH.name}
	</a>
	{if isset($BRANCH.children)}
    <ul class="dropdown-menu drp-nav">
		{$BRANCH.children}
	</ul>
	{/if}
</li>
