<script>
  import {
    Header,
    HeaderName,
    HeaderMenuButton,
    HeaderNav,
    HeaderNavItem,
    SideNav,
    SideNavItems,
    SideNavLink
  } from "carbon-components-svelte";

  export let onNavigate = (path) => {};
  export let onGenerateReport = () => {};
  export let onLogout = () => {};

  let isSideNavOpen = false;
</script>

<Header aria-label="CowlibrateAI Dashboard">
  <!-- Hamburger menu (mobile) -->
  <HeaderMenuButton
    aria-label="Open menu"
    isActive={isSideNavOpen}
    on:click={() => (isSideNavOpen = !isSideNavOpen)}
  />

  <HeaderName prefix="">CowlibrateAI</HeaderName>

  <!-- Desktop Nav -->
  <HeaderNav class="desktop-nav">
    <HeaderNavItem on:click={() => onNavigate('/cow')}>Bovine Entry</HeaderNavItem>
    <HeaderNavItem on:click={() => onNavigate('/dbview')}>Herd View</HeaderNavItem>
    <HeaderNavItem on:click={onGenerateReport}>Generate Report</HeaderNavItem>
    <HeaderNavItem on:click={onLogout}>Logout</HeaderNavItem>
  </HeaderNav>
</Header>

<!-- Mobile Side Nav -->
<SideNav
  expanded={isSideNavOpen}
  on:overlay-click={() => (isSideNavOpen = false)}
>
  <SideNavItems>
    <SideNavLink on:click={() => { onNavigate('/cow'); isSideNavOpen = false; }}>
      Bovine Entry
    </SideNavLink>
    <SideNavLink on:click={() => { onNavigate('/dbview'); isSideNavOpen = false; }}>
      Herd View
    </SideNavLink>
    <SideNavLink on:click={() => { onGenerateReport(); isSideNavOpen = false; }}>
      Generate Report
    </SideNavLink>
    <SideNavLink on:click={() => { onLogout(); isSideNavOpen = false; }}>
      Logout
    </SideNavLink>
  </SideNavItems>
</SideNav>

<style>
  .desktop-nav {
  display: none;
}

@media (min-width: 768px) {
  .desktop-nav {
    display: flex;
  }

  :global(.bx--header__menu-button) {
    display: none;
  }
}

</style>