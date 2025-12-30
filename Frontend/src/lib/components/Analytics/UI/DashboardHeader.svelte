<script>
  import {
    Header,
    HeaderNav,
    HeaderNavItem,
    SideNav,
    SideNavItems,
    SideNavLink
  } from "carbon-components-svelte";

  let isSideNavOpen = false;

  export let onNavigate = (path) => {};
  export let onGenerateReport = () => {};
  export let onLogout = () => {};
</script>

<Header company="CowlibrateAI Dashboard">
  <!-- Fake hamburger using button -->
  <button
    class="menu-btn"
    on:click={() => (isSideNavOpen = !isSideNavOpen)}
    aria-label="Menu"
  >
    ☰
  </button>

  <HeaderNav class="desktop-nav">
    <HeaderNavItem on:click={() => onNavigate('/cow')}>Bovine Entry</HeaderNavItem>
    <HeaderNavItem on:click={() => onNavigate('/dbview')}>Herd View</HeaderNavItem>
    <HeaderNavItem on:click={onGenerateReport}>Generate Report</HeaderNavItem>
    <HeaderNavItem on:click={onLogout}>Logout</HeaderNavItem>
  </HeaderNav>
</Header>

<SideNav expanded={isSideNavOpen}>
  <SideNavItems>
    <SideNavLink on:click={() => onNavigate('/cow')}>Bovine Entry</SideNavLink>
    <SideNavLink on:click={() => onNavigate('/dbview')}>Herd View</SideNavLink>
    <SideNavLink on:click={onGenerateReport}>Generate Report</SideNavLink>
    <SideNavLink on:click={onLogout}>Logout</SideNavLink>
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