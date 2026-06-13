
export async function initPagosBanco() {

    try {

        const response = await fetch('/charts/pagosBanco/');
        const datos = await response.json();
        console.log(datos);

        let fechas = [];
        let bancos = [];
        let series = [];
        // Obtener fechas únicas
        for(let i = 0; i < datos.length; i++){
            if(!fechas.includes(datos[i].fecha_pago)){
                fechas.push(datos[i].fecha_pago);
            }
        }
        // Obtener bancos únicos
        for(let i = 0; i < datos.length; i++){
            if(!bancos.includes(datos[i].banco__nombre)){
                bancos.push(datos[i].banco__nombre);
            }
        }
        // Crear una línea por banco
        for(let i = 0; i < bancos.length; i++){
            let banco = bancos[i];
            let montos = [];
            for(let j = 0; j < fechas.length; j++){
                let fecha = fechas[j];
                let total = 0;
                for(let k = 0; k < datos.length; k++){
                    if(
                        datos[k].fecha_pago == fecha &&
                        datos[k].banco__nombre == banco
                    ){
                        total = datos[k].total;
                        break;
                    }
                }
                montos.push(total);
            }
            series.push({
                name: banco,
                type: "bar",
                data: montos
            });

        }

        const chart = echarts.init(document.getElementById("fondosBancoChart"));

        chart.setOption({
            title: {
                
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {},
            toolbox: {
                show: true,
                feature: {
                    dataView: {
                        show: true,
                        readOnly: false
                    },
                    magicType: {
                        show: true,
                        type: ['line', 'bar']
                    },
                    restore: {
                        show: true
                    },
                    saveAsImage: {
                        show: true
                    }
                }
            },
            xAxis: {
                type: 'category',
                data: fechas
            },
            yAxis: {
                type: 'value'
            },
            series:series
        });
    }

    catch(error) {

        console.error(
            "Se detectó un problema:",
            error.message
        );

    }

}