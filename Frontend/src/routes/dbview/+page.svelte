<script>
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import DBNav from "$lib/components/DatabaseView/DBNav.svelte";
  import DatabaseView from "$lib/components/DatabaseView/DatabaseView.svelte";
  import { Header, HeaderNav, HeaderNavItem, FileUploaderButton } from "carbon-components-svelte";

  let entries = [];
  let loading = true;
  let error = null;

  onMount(async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) goto("/login");

      const res = await fetch(
        "https://cowlibrate.onrender.com/api/submissions",
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        }
      );

      if (!res.ok) throw new Error("Failed to load submissions.");

      entries = await res.json();
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  });

  function navigate(path) {
    goto(path);
  }

  async function generateReport() {
    const { jsPDF } = await import("jspdf");
    const html2canvas = (await import("html2canvas")).default;

    const dashboardEl = document.getElementById("dashboard");
    if (!dashboardEl) return;

    const canvas = await html2canvas(dashboardEl, { scale: 2 });
    const imgData = canvas.toDataURL("image/png");

    const pdf = new jsPDF("p", "pt", "a4");
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

    pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
    pdf.save("Goat-Analytics-Report.pdf");
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    goto("/login");
  }
</script>

<DashboardHeader
  onNavigate={navigate}
  onGenerateReport={generateReport}
  onLogout={logout}
/>

<main id="dashboard">
  {#if loading}
    <p>Loading your submissions...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else}
    <DatabaseView {entries} />
  {/if}
</main>

<style>
  main#dashboard {
    max-width: 1200px;
    width: 90%;
    margin: 5rem auto 3rem;
    padding: 1rem;
  }

  .error {
    color: red;
  }
</style>
