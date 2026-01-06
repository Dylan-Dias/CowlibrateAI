<script>
  import {
    Header,
    HeaderNav,
    HeaderNavItem
  } from "carbon-components-svelte";
  import { goto } from "$app/navigation";


    function navigateTo(path) {
    goto(path);
  }
</script>

<Header company="Dairy Dashboard" platformName="Milk Yield">
  <HeaderNav>
    <HeaderNavItem on:click={() => navigateTo("/analytics")}>
      Bovine Analytics
    </HeaderNavItem>
      <HeaderNavItem on:click={() => navigateTo('/dbview')}>
        Herd View
    </HeaderNavItem>

    <HeaderNavItem>
      <FileUploaderButton
        buttonLabel="Upload Excel"
        accept={[".xlsx", ".xls"]}
        multiple={false}
        on:change={(e) => onFileUpload(e.detail.files)}
      />
    </HeaderNavItem>
    
  </HeaderNav>
</Header>