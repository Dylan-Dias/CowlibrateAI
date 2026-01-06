<script>
  import {
    Header,
    HeaderNav,
    HeaderNavLink
  } from "carbon-components-svelte";

  export let onNavigate = (path) => {};
  export let onGenerateReport = () => {};
  export let onLogout = () => {};
</script>

<Header company="CowlibrateAI" platformName="Dashboard">
  <HeaderNav>
    <HeaderNavLink href="/analytics" on:click={e => { e.preventDefault(); onNavigate("/analytics"); }}>
      Bovine Analytics
    </HeaderNavLink>

    <HeaderNavLink as="button" on:click={onGenerateReport}>
      Generate Report
    </HeaderNavLink>

    <HeaderNavLink as="button" on:click={onLogout}>
      Logout
    </HeaderNavLink>
  </HeaderNav>
</Header>
