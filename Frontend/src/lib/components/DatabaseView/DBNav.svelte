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

<Header company="CowlibrateAI" platformName="Dashboard">
  <!-- Desktop Nav -->
  <HeaderNav>
    <HeaderNavItem on:click={() => onNavigate('/cow')}>Bovine Entry</HeaderNavItem>
    <!-- <HeaderNavItem on:click={() => onNavigate('/dbview')}>Herd View</HeaderNavItem> -->
    <HeaderNavItem on:click={onGenerateReport}>Generate Report</HeaderNavItem>
    <HeaderNavItem on:click={onLogout}>Logout</HeaderNavItem>
  </HeaderNav>
</Header>

