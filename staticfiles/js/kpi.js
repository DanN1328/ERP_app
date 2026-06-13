export async function cargarKPIs() {

    const response = await fetch('/charts/dashboardskpi/');
    const data = await response.json();

    document.getElementById('kpiFondos').textContent = Number(data.Fondos_Totales).toFixed(2) + "$MXN";
    document.getElementById('kpiGastos').textContent = data.Gastos_Pendientes;
    document.getElementById('kpiPagos').textContent = data.Pagos_Pendientes;
    document.getElementById('kpiClientes').textContent = data.Clientes;

}