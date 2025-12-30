<script>
  import {
    Header,
    SideNav,
    SideNavItems,
    SideNavLink
  } from "carbon-components-svelte";

  let sideNavOpen = false;

  export let onNavigate = (path) => {};
  export let onGenerateReport = () => {};
  export let onLogout = () => {};
</script>

<!-- HEADER (Carbon’s built‑in hamburger works automatically) -->
<Header
  company="CowlibrateAI Dashboard"
  on:menu-toggle={() => (sideNavOpen = !sideNavOpen)}
>
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

<!-- MAIN CONTENT -->
<main class="content">
  <slot />
</main>

<style>
  /* Keep header above everything */
  header.bx--header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 8000;
  }

  /* Prevent content from hiding under header */
  .content {
    padding-top: 3rem;
  }

  /* Ensure SideNav overlays correctly */
  :global(.bx--side-nav) {
    z-index: 7000;
  }

  /* Prevent layout clipping */
  :global(html),
  :global(body) {
    margin: 0;
    padding: 0;
    overflow-x: hidden;
  }
</style>
