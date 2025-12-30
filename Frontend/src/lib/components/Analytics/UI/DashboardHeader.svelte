<script>
  import { Header, SideNav, SideNavItems, SideNavLink } from "carbon-components-svelte";

  let sideNavOpen = false;

  export let onNavigate = (path) => {};
  export let onGenerateReport = () => {};
  export let onLogout = () => {};
</script>

<Header company="CowlibrateAI Dashboard" on:menu-toggle={() => (sideNavOpen = !sideNavOpen)}>
  <!-- No custom button needed -->
</Header>

<SideNav expanded={sideNavOpen} on:overlay-click={() => (sideNavOpen = false)}>
  <SideNavItems>
    <SideNavLink on:click={() => { onNavigate('/cow'); sideNavOpen = false; }}>
      Bovine Entry
    </SideNavLink>
    <SideNavLink on:click={() => { onNavigate('/dbview'); sideNavOpen = false; }}>
      Herd View
    </SideNavLink>
    <SideNavLink on:click={() => { onGenerateReport(); sideNavOpen = false; }}>
      Generate Report
    </SideNavLink>
    <SideNavLink on:click={() => { onLogout(); sideNavOpen = false; }}>
      Logout
    </SideNavLink>
  </SideNavItems>
</SideNav>
