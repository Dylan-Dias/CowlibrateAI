<script>
  import {
    Header,
    HeaderName,
    SideNav,
    SideNavItems,
    SideNavLink
  } from "carbon-components-svelte";

  let sideNavOpen = false;

  export let onNavigate = (path) => {};
  export let onGenerateReport = () => {};
  export let onLogout = () => {};
</script>

<!-- HEADER (Carbon built-in hamburger works automatically) -->
<Header on:menu-toggle={() => (sideNavOpen = !sideNavOpen)}>
  <HeaderName>CowlibrateAI Dashboard</HeaderName>
</Header>

<!-- SIDENAV (Carbon handles mobile vs desktop automatically) -->
<SideNav
  expanded={sideNavOpen}
  on:overlay-click={() => (sideNavOpen = false)}
>
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

<!-- MAIN CONTENT AREA -->
<main class="content">
  <slot />
</main>

<style>
  /* Ensure the header stays above everything */
  header.bx--header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 8000;
  }

  /* Prevent content from hiding under the header */
  .content {
    padding-top: 3rem;
  }

  /* Ensure SideNav can slide over content */
  :global(.bx--side-nav) {
    z-index: 7000;
  }

  /* Fix layout so nothing clips the SideNav */
  :global(body),
  :global(html) {
    margin: 0;
    padding: 0;
    overflow-x: hidden;
  }
</style>
