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

  export let navigateTo = (path) => {};
  export let onGenerateReport = () => {};
  export let onLogout = () => {};

  let isSideNavOpen = false;
</script>

<Header company="CowlibrateAI" platformName="Dashboard">
 
  <HeaderNav>
    <HeaderNavItem on:click={() => navigateTo("/analytics")}>Bovine Analytics</HeaderNavItem>
    <HeaderNavItem on:click={onGenerateReport}>Generate Report</HeaderNavItem>
    <HeaderNavItem on:click={onLogout}>Logout</HeaderNavItem>
  </HeaderNav>
</Header>

