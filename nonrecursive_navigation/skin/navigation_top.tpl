<li{if isset($BRANCH.children)} class="dropdown"{/if}>
	<a class="btn-nav" href="{$BRANCH.url}" title="{$BRANCH.name}">
		{$BRANCH.name}
		{if isset($BRANCH.children)}<span class="caret"></span>{/if}
	</a>
	{if isset($BRANCH.children)}
    <ul class="dropdown-menu multi-level drp-nav" role="menu" aria-labelledby="dropdownMenu">
		{$BRANCH.children}
	</ul>
	{/if}
</li>
