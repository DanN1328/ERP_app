export async function initGastosCliente() {
    try {
        const response = await fetch('/charts/gastosCliente/');
        const datos = await response.json();

        let serie = [];

        for(let i = 0; i < datos.length; i++) {

            serie.push({
                name: datos[i].cliente_id__nombre,
                value: datos[i].total
            });

        }

        const chart = echarts.init(document.getElementById("gastosClienteChart"));
        
        chart.setOption(
            {

                tooltip: {
                },
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },

                legend: {
                    orient: 'vertical',
                    left: 'left'
                },

                series: [
                    {
                        name: 'Gastos',
                        type: 'pie',
                        radius: '70%',
                        data: serie
                    }
                ]
            }
        );
    }
    catch (error) {
    console.error("Se detectó un problema: ", error.message);
    }
}