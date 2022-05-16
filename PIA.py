# ===> Importaciones <===
import sys
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from   datetime import datetime
from   PyQt5 import uic, QtGui
from   PyQt5.QtCore import *
from   PyQt5.QtGui import *
from   PyQt5.QtWidgets import *

# variable global
user = []
# =============================
# =   Modulo Acceso - Login   =
# =============================
class Login(QMainWindow):
    def __init__(self, parent = None):
        super(Login, self).__init__(parent)
        uic.loadUi(r'UI/login.ui', self)
        
        global user
        self.user = user
        self.UiLogin()
        
    def UiLogin(self):
        self.btnAccess.clicked.connect(self.fnAcceso)

    def fnAcceso(self):
        usuario  = self.txtUser.text()
        pswd     = self.txtPassword.text()
        val      = (usuario, pswd)
        
        con      = conexion()
        c        = con.cursor()
        sql = '''
            SELECT * FROM empleados
            WHERE nickname = %s AND contrasenia = %s;
        '''
        c.execute(sql, val)
        data = c.fetchall()

        if data:
            self.user.append(data[0][0].upper())
            self.user.append(data[0][1].upper())
            self.user.append(data[0][2].upper())

            if data[0][6] == self.cmbUser.currentIndex():
                self.fnModulos()

            elif data[0][6] == 2:
                self.fnVentas()

            else:
                self.lblEstado.setText('Acceso denegado')
        else:
            self.lblEstado.setText('Usuario o contraseña\nincorrectos.')

    def fnModulos(self):
        self.hide()
        vModulos = Modulos(self)
        vModulos.show()

    def fnVentas(self):
        self.hide()
        vVentas = Ventas(self)
        vVentas.show()

# =======================
# =   Menú de modulos   =
# =======================
class Modulos(QMainWindow):
    def __init__(self, parent = None):
        super(Modulos, self).__init__(parent)
        uic.loadUi(r'UI/Ui_Modulos.ui', self)
        self.UiModulos()
    
    def UiModulos(self):
        self.lblUsuario.setText(f'{user[0]} - {user[1]} {user[2]}')
        self.btnEmpleados.clicked.connect(self.fnEmpleados)
        self.btnClientes.clicked.connect(self.fnClientes)
        self.btnProductos.clicked.connect(self.fnProductos)
        self.btnVentas.clicked.connect(self.fnVentas)
        self.btnInventario.clicked.connect(self.fnInventario)
    
    def fnClientes(self):
        self.hide()
        vClientes = Clientes(self)
        vClientes.show()
    
    def fnEmpleados(self):
        self.hide()
        vEmpleados = Empleados(self)
        vEmpleados.show()

    def fnProductos(self):
        self.hide()
        vProductos = Productos(self)
        vProductos.show()

    def fnVentas(self):
        self.hide()
        vVentas = Ventas(self)
        vVentas.show()
    
    def fnInventario(self):
        self.hide()
        vInventario = Inventario(self)
        vInventario.show()


# ===========================
# =        Módulos          =
# ===========================
class Empleados(QMainWindow):
    def __init__(self, parent = None):
        super(Empleados, self).__init__(parent)
        uic.loadUi(r'UI/Ui_Empleados.ui', self)
        self.UiEmpleados()

    # ===>   Inicialización de empleados   <===
    def UiEmpleados(self):
        self.Carga()
        self.lblUsuario.setText(f'{user[0]} - {user[1]} {user[2]}')
        
        self.btnNuevoE.clicked.connect(self.RegistroE)
        self.btnBuscarE.clicked.connect(self.BuscarE)
        self.btnEliminarE.clicked.connect(self.EliminarE)
        self.btnLimpiarE.clicked.connect(self.fnLimpiar)
        self.btnVolverE.clicked.connect(self.fnVolver)
        self.btnRefresh.clicked.connect(self.Carga)
    
    def Carga(self):
        con = conexion()
        reg = fnCarga(con, 'empleados')
        
        numero = self.tbwEmpleados.rowCount()
        for fila in range(numero):
            self.tbwEmpleados.removeRow(0)

        for registro in reg:
            fila = self.tbwEmpleados.rowCount()
            self.tbwEmpleados.insertRow(fila)
            for d in range(len(registro)):
                dato = registro[d]
                self.tbwEmpleados.setItem(fila, d, QTableWidgetItem(str(dato)))
    
    def RegistroE(self):
        self.hide()
        vRegistroE = RegistroE(self)
        vRegistroE.show()
    
    def BuscarE(self):
        empleado = (self.txtEmpleado.text(),)
        con = conexion()
        c = con.cursor()
        sql = '''
            SELECT * FROM empleados
            WHERE id_empleado = %s
        '''
        c.execute(sql, empleado)
        data = c.fetchall()

        if data:
            puestos = [
                'Administrador',
                'Cajero',
                'Vendedor',
                'Promotor',
                'Limpieza'
            ]
            for puesto in range(len(puestos)):
                if data[0][6] == puesto + 1:
                    p = puesto + 1
                    break

            msj = f'''
            --- Resultado de búsqueda ---
            Empleado: {data[0][0]}
            {data[0][1]} {data[0][2]}
            Fecha Nacimiento: {data[0][3]}
            Puesto: {p}
            Correo: {data[0][7]}
            Telefono: {data[0][8]}
            '''
        else:
            msj = 'Empleado no encontrado'
        
        self.txtPrint.clear()
        self.txtPrint.append(msj)


    def EliminarE(self):
        registro = self.tbwEmpleados.currentRow()
        empleado = str(self.tbwEmpleados.item(registro, 0).text())
        print(registro, empleado)

        con = conexion()
        c = con.cursor()
        sql = '''
            DELETE FROM empleados
            WHERE id_empleado = %s;
        '''
        c.execute(sql, (empleado,))
        con.commit()

        if c.rowcount > 0:
            self.tbwEmpleados.removeRow(registro)
            msj = f'\nEmpleado {empleado} eliminado.'
        else:
            msj = f'\nError!\nEmpleado no encontrado en BD'
        
        self.txtPrint.clear()
        self.txtPrint.append(msj)

    def fnLimpiar(self):
        self.txtEmpleado.clear()
        self.txtPrint.clear()
    
    def fnVolver(self):
        self.parent().show()
        self.close()


class Clientes(QMainWindow):
    def __init__(self, parent = None):
        super(Clientes, self).__init__(parent)
        uic.loadUi(r'UI/Ui_Clientes.ui', self)
        self.UiClientes()
    
    def UiClientes(self):
        self.Carga()
        self.lblUsuario.setText(f'{user[0]} - {user[1]} {user[2]}')

        self.btnNuevoC.clicked.connect(self.RegistroC)
        self.btnBuscarC.clicked.connect(self.BuscarC)
        self.btnEliminarC.clicked.connect(self.EliminarC)
        self.btnLimpiarC.clicked.connect(self.fnLimpiar)
        self.btnVolverC.clicked.connect(self.Volver)
        self.btnRefresh.clicked.connect(self.Carga)
    
    def Carga(self):
        con = conexion()
        data = fnCarga(con, 'clientes')

        numero = self.tbwClientes.rowCount()
        for fila in range(numero):
            self.tbwClientes.removeRow(0)

        for registro in data:
            fila = self.tbwClientes.rowCount()
            self.tbwClientes.insertRow(fila)
            for d in range(len(registro)):
                dato = registro[d]
                self.tbwClientes.setItem(fila, d, QTableWidgetItem(str(dato)))

    def RegistroC(self):
        self.hide()
        vRegistroC = RegistroC(self)
        vRegistroC.show()
    
    def BuscarC(self):
        cliente = (int(self.txtCliente.text()),)

        con = conexion()
        c = con.cursor()
        sql = 'SELECT * FROM clientes WHERE id_cliente = %s'
        c.execute(sql, cliente)
        data = c.fetchall()

        msj = f'''
        --- Resultado de la búsqueda ---
        No. Cliente: {data[0][0]}
        Nombre: {data[0][1]} {data[0][2]}

        Dirección: {data[0][3]}
        Correo: {data[0][4]}

        Estado: {"Activo" if data[0][5] == 1 else "Inactivo"}
        Lim. Crédito:     ${data[0][6]}
        Saldo disponible: ${data[0][7]}
        '''
        self.txtPrint.clear()
        self.txtPrint.append(msj)
    

    def EliminarC(self):
        registro = self.tbwClientes.currentRow()
        cliente = (self.tbwClientes.item(registro, 0).text(),)

        con = conexion()
        c = con.cursor()
        sql = '''
            DELETE FROM clientes
            WHERE id_cliente = %s;
        '''
        c.execute(sql, cliente)
        con.commit()

        if c.rowcount > 0:
            self.tbwClientes.removeRow(registro)
            msj = f'Cliente {cliente} eliminado.'
        else:
            msj = f'Cliente no encontrado en BD'
        
        self.txtPrint.clear()
        self.txtPrint.append(msj)


    def fnLimpiar(self):
        self.txtCliente.clear()
        self.txtPrint.clear()


    def Volver(self):
        self.parent().show()
        self.close()


class Productos(QMainWindow):
    def __init__(self, parent = None):
        super(Productos, self).__init__(parent)
        uic.loadUi(r'UI/Ui_Productos.ui', self)
        self.UiProductos()
    
    def UiProductos(self):
        self.txtCosto.setValidator(QDoubleValidator(0.99, 99.99, 2))
        self.txtPrecio.setValidator(QDoubleValidator(0.99, 99.99, 2))

        con = conexion()
        reg = fnCarga(con, 'productos')
        for registro in reg:
            fila = self.tbwProductos.rowCount()
            self.tbwProductos.insertRow(fila)

            for d in range(len(registro)):
                dato = registro[d]
                self.tbwProductos.setItem(fila, d, QTableWidgetItem(str(dato)))
        
        reg = fnCarga(con, 'categoria')
        for registro in reg:
            self.cmbCategoriaP.addItem(registro[1])

        self.btnRegistrarP.clicked.connect(self.Registro)
        self.btnBuscarP.clicked.connect(self.Busqueda)
        self.btnEliminarP.clicked.connect(self.Eliminar)
        self.btnLimpiarP.clicked.connect(self.Limpiar)
        self.btnVolverP.clicked.connect(self.fnVolver)
        self.btnReporte.clicked.connect(self.Reporte)


    def Registro(self):
        codigo      = self.txtCodigoP.text()
        descripcion = self.txtDescripcionP.text()
        categoria   = (self.cmbCategoriaP.currentIndex() + 1) * 100
        costo       = self.txtCosto.text()
        precio      = self.txtPrecio.text()
        dia         = self.dtCompraP.date().day()
        mes         = self.dtCompraP.date().month()
        anio        = self.dtCompraP.date().year()
        
        valores = (codigo, descripcion, int(categoria), float(costo), float(precio), f'{anio}-{mes}-{dia}')
        con = conexion()
        c = con.cursor()
        sql = '''
            INSERT INTO productos (codigo, descripcion, categoria, costo, precio, fec_compra)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
        c.execute(sql, valores)
        con.commit()

        f = self.tbwProductos.rowCount()
        self.tbwProductos.insertRow(f)

        for d in range(len(valores)):
            dato = valores[d]
            self.tbwProductos.setItem(f, d, QTableWidgetItem(str(dato)))

        self.txtCodigoP.clear()
        self.txtDescripcionP.clear()
        self.cmbCategoriaP.setCurrentIndex(-1)
        self.txtCosto.clear()
        self.txtPrecio.clear()

    def Busqueda(self):
        producto = (self.txtProducto.text(),)

        con = conexion()
        c = con.cursor()
        sql = '''
        SELECT * FROM productos
        WHERE codigo = %s
        '''
        c.execute(sql, producto)
        data = c.fetchall()
        
        if data:
            categorias = [
                'Telefonia',
                'Equipo de computo',
                'Gamming',
                'Electrónica',
                'Accesorios',
                'Refacciones'
            ]
            if data[0][2] == 100:
                categoria = categorias[0]
            elif data[0][2] == 200:
                categoria = categorias[1]
            elif data[0][2] == 300:
                categoria = categorias[2]
            elif data[0][2] == 400:
                categoria = categorias[3]
            elif data[0][2] == 500:
                categoria = categorias[4]
            elif data[0][2] == 600:
                categoria = categorias[6]
            
            msj = f'''
            --- Resultado de Búsqueda ---
            Categoria: {categoria}
            Producto:
            {data[0][0]} | {data[0][1]}

            Costo: ${data[0][3]}
            Precio: ${data[0][4]}
            Fecha de compra: {data[0][5]}
            '''
        else:
            msj = 'No se encontró el producto'
        
        self.txtPrint.clear()
        self.txtPrint.append(msj)
    
    def Eliminar(self):
        registro = self.tbwProductos.currentRow()
        producto = (self.tbwProductos.item(registro, 0).text(),)

        con = conexion()
        c = con.cursor()
        sql = '''
            DELETE FROM productos
            WHERE codigo = %s
        '''
        c.execute(sql, producto)
        con.commit()

        if c.rowcount > 0:
            self.tbwProductos.removeRow(registro)
            msj = f'\nProducto eliminado correctamente.'
        else:
            msj = f'\nNo se encontró producto.'
        
        self.txtPrint.clear()
        self.txtPrint.append(msj)

    def Reporte(self):
        con = conexion()
        c = con.cursor()
        sql = f'''
            SELECT producto, sum(cantidad)
            FROM ventas_detalle
            GROUP BY producto
            ORDER BY sum(cantidad) DESC
            limit 5;
        '''
        c.execute(sql)
        data = c.fetchall()

        productos = []
        ventas = []
        for p in data:
            producto = self.fnProducto(p[0])
            productos.append(producto[0][0])
            ventas.append(p[1])
        
        x = np.array(productos)
        y = np.array(ventas)

        plt.bar(x, y, color = '#09172e')
        plt.title('Productos más vendidos')
        plt.show()

    def fnProducto(self, codigo):
        con = conexion()
        c = con.cursor()
        sql = f'''
            SELECT descripcion
            FROM productos
            WHERE codigo = {codigo};
        '''
        c.execute(sql)
        producto = c.fetchall()
        return producto

    def Limpiar(self):
        self.txtProducto.clear()
        self.txtPrint.clear()
    
    def fnVolver(self):
        self.parent().show()
        self.close()


class Ventas(QMainWindow):
    def __init__(self, parent = None):
        super(Ventas, self).__init__(parent)
        uic.loadUi(r'UI/Ui_Ventas.ui', self)
        self.UiVentas()

    def UiVentas(self):
        con = conexion()
        sucursales = fnCarga(con, 'sucursal')
        for sucursal in sucursales:
            self.cmbSucursales.addItem(f'{sucursal[1]}')

        self.lblCajero.setText(f'{user[0]} - {user[1]} {user[2]}')
        self.lblFecha.setText(f'Fecha: {datetime.today().strftime("%Y-%m-%d")}')

        self.lblEstado.setHidden(True)
        self.lblEstado_2.setHidden(True)

        self.btnValidar.clicked.connect(self.fnValidar)
        self.btnAgregarP.clicked.connect(self.Lista)
        self.btnTerminar.clicked.connect(self.fnTerminarC)
        self.btnEliminar.clicked.connect(self.fnEliminar)
        self.btnRegistrarC.clicked.connect(self.Finalizar)
        self.btnCancelar.clicked.connect(self.fnLimpiar)
        self.btnLimpiar.clicked.connect(self.fnLimpiar_2)
        self.btnVolver.clicked.connect(self.fnVolver)
        self.btnReporte.clicked.connect(self.Reporte)

    def fnValidar(self):
        cliente = self.cliente()

        if cliente:
            self.lblEstado_2.setHidden(False)
            self.lblEstado.setHidden(True)
            self.txtCodigo.setEnabled(True)
            self.spbCantidad.setEnabled(True)
            self.txtSaldo.setText(f'{cliente[0][-1]:,.2f}')
        else:
            self.txtClienteV.clear()
            self.lblEstado_2.setHidden(True)
            self.lblEstado.setHidden(False)

    def Lista(self):
        producto = (self.txtCodigo.text(),)
        cantidad = self.spbCantidad.value()

        if cantidad > 0:
            con = conexion()
            c   = con.cursor()
            sql = '''
                SELECT codigo, descripcion, precio
                FROM productos
                WHERE codigo = %s;
            '''
            c.execute(sql, producto)
            data = c.fetchall()

            self.lstCant.addItem(str(cantidad))
            self.lstDescripcion.addItem(f'{data[0][0]}  {data[0][1]}')
            self.lstPrecio.addItem(str(data[0][2]))

            self.txtCodigo.clear()
            self.spbCantidad.setValue(0)
            self.fnCuenta()

    def fnTerminarC(self):
        self.cmbTipoCompra.setEnabled(True)
        self.validadorV()

    def Finalizar(self):
        if self.cmbTipoCompra.currentIndex() == 0:
            pago = self.fnCuenta()
            recibe = float(self.txtRecibe.text())
            if recibe >= pago:
                cambio = recibe - pago
                self.Venta(0)
                self.VentaD()
                self.fnTicket(0, self.fnCuenta(), recibe, cambio, 0)
                self.fnLimpiar()
            else:
                self.lblMsj.setText('')
                self.lblMsj.setText('¡Monto recibido insuficiente!')
        else:
            c_data = self.cliente()
            saldo = c_data[0][-1]
            credito = self.fnCuenta()
            if credito > saldo:
                self.lblMsj.setText('')
                self.lblMsj.setText('¡Saldo insuficiente!')
            else:
                n_saldo = saldo - credito
                self.Venta(1)
                self.VentaD()
                self.fnTicket(1, self.fnCuenta(), 0, 0, n_saldo)
                self.fnLimpiar()

    def Venta(self, tipo):
        self.tipo = tipo
        con = conexion()
        c = con.cursor()

        fecha = datetime.today().strftime('%Y-%m-%d')
        sucursal = (self.cmbSucursales.currentIndex() + 1) * 1000
        importe = self.fnCuenta()
        cliente = self.cliente()
        cajero = user[0]
        valores = (fecha, sucursal, importe, cliente[0][0], cajero)
        
        sql = '''
            INSERT INTO ventas (fecha, sucursal, importe, cliente, cajero)
            VALUES (%s, %s, %s, %s, %s);
        '''
        c.execute(sql, valores)
        con.commit()

        if self.tipo == 1:
            saldo = cliente[0][-1] - importe
            sql = '''
                UPDATE clientes
                SET saldo = %s
                WHERE id_cliente = %s
            '''
            c.execute(sql, (saldo, cliente[0][0]))
        
    def Reporte(self):
        con = conexion()
        c = con.cursor()
        sql = '''
            SELECT sucursal, sum(importe)
            FROM ventas
            GROUP BY sucursal
            ORDER BY sum(importe) DESC;
        '''
        c.execute(sql)
        data = c.fetchall()
        
        sucursal = []
        importe = []
        for d in data:
            sucursal.append(d[0])
            importe.append(d[1])
        
        x = np.array(sucursal)
        y = np.array(importe)

        plt.plot(y, ls = '--')
        plt.title('Ventas por sucursal')
        plt.show()


    def fnTicket(self, tipo, importe, pago, cambio, saldo):
        f_prod = ''
        d_cliente = self.cliente()
        for p in range(self.lstCant.count()):
            cantidad = int(self.lstCant.item(p).text())
            producto = self.lstDescripcion.item(p).text()
            precio   = float(self.lstPrecio.item(p).text())
            
            f_prod += f'{cantidad:<5}{producto:<45}{precio:>10,.2f}\n\t'
        
        total = f'{"Total:  $":>60}{importe:>10,.2f}'
        f_pago = f'{"Recibido:  $":>60}{pago:>10,.2f}'
        f_cambio = f'{"Cambio:  $":>60}{cambio:>10,.2f}'
        f_saldo = f'{"Saldo disponible:  $"}{saldo:>10,.2f}'

        if tipo == 0:
            msj = f'''
                {"===  TOPES DE GAMA  ===":^60}
                "Sucursal:" {self.cmbSucursales.currentText():<20}{"Cajero":>20} {user[0]:>10}
                Cliente: {d_cliente[0][0]} | {d_cliente[0][1]} {d_cliente[0][2]}
                
                {f_prod}
                {"-" * 60}
                {total}
                {f_pago}
                {f_cambio}

                {"===  GRACIAS POR SU COMPRA  ==="}
            '''
        else:
            msj = f'''
                {"===  TOPES DE GAMA  ===":^60}
                "Sucursal:" {self.cmbSucursales.currentText():<20}{"Cajero":>20} {user[0]:>10}
                Cliente: {d_cliente[0][0]} | {d_cliente[0][1]} {d_cliente[0][2]}
                
                {f_prod}
                {"-" * 60}
                {total}
                {f_saldo}

                {"===  GRACIAS POR SU COMPRA  ===":^60}
            '''
        self.txtTicket.clear()
        self.txtTicket.append(msj)
        
    def validadorV(self):
        self.cmbTipoCompra.currentTextChanged.connect(self.fnTipoCompra)

    def fnTipoCompra(self):
        importe = self.fnCuenta()

        if self.cmbTipoCompra.currentIndex() == 0:
            self.txtPago.setEnabled(True)
            self.txtRecibe.setEnabled(True)
            self.txtPago.setText(f'{importe:,.2f}')
            self.txtCredito.clear()
        else:
            self.txtPago.setEnabled(False)
            self.txtRecibe.setEnabled(False)
            self.txtCredito.setText(f'{importe:,.2f}')

    def VentaD(self):
        con = conexion()
        c = con.cursor()
        sql = '''
            SELECT no_venta
            FROM ventas
            ORDER BY no_venta DESC
            LIMIT 1;
        '''
        c.execute(sql)
        venta = c.fetchall()

        for prod, cant in zip(range(self.lstDescripcion.count()), range(self.lstCant.count())):
            cantidad = int(self.lstCant.item(cant).text())
            prod     = self.lstDescripcion.item(prod).text()
            codigo   = prod[:5]
            valores  = (venta[0][0], codigo, cantidad)
            
            sql = '''
                INSERT INTO ventas_detalle(no_venta, producto, cantidad)
                VALUES (%s, %s, %s)
            '''
            c.execute(sql, valores)
            con.commit()

    def cliente(self):
        cliente = (self.txtClienteV.text(),)
        con = conexion()
        c = con.cursor()
        sql = '''
            SELECT id_cliente, nombre, apellido, credito, saldo
            FROM clientes
            WHERE id_cliente = %s
        '''
        c.execute(sql, cliente)
        data = c.fetchall()
        return data

    def fnCuenta(self):
        total = 0
        for c, p in zip(range(self.lstCant.count()), range(self.lstPrecio.count())):
            cant = int(self.lstCant.item(c).text())
            prec = float(self.lstPrecio.item(p).text())
            subtotal = cant * prec
            total += subtotal
            self.lblTotal.setText(f'${total:,.2f} MX')
        
        return total

    def fnEliminar(self):
        fila = self.lstDescripcion.currentRow()
        self.lstCant.takeItem(fila)
        self.lstDescripcion.takeItem(fila)
        self.lstPrecio.takeItem(fila)
        self.fnCuenta()
    
    def fnLimpiar(self):
        self.txtClienteV.clear()
        self.cmbTipoCompra.setCurrentIndex(-1)
        self.txtSaldo.clear()
        self.txtCredito.clear()
        self.txtPago.clear()
        self.txtRecibe.clear()
        self.lblMsj.setText('')
        self.lblTotal.setText('$0.00 MX')

        for i in range(self.lstCant.count()):
            self.lstCant.takeItem(0)
            self.lstDescripcion.takeItem(0)
            self.lstPrecio.takeItem(0)
    
    def fnLimpiar_2(self):
        self.txtTicket.clear()
    
    def fnVolver(self):
        self.parent().show()
        self.close()

class Inventario(QMainWindow):
    def __init__(self, parent = None):
        super(Inventario, self).__init__(parent)
        uic.loadUi(r'UI/Ui_Almacen.ui', self)
        self.UiInvenatario()

    def UiInvenatario(self):
        con = conexion()
        sucursales = fnCarga(con, 'sucursal')
        for sucursal in sucursales:
            self.cmbSucursal.addItem(f'{sucursal[1]}')

        data = fnCarga(con, 'almacen')
        for registro in data:
            fila = self.tbwRegistros.rowCount()
            self.tbwRegistros.insertRow(fila)

            for d in range(len(registro)):
                dato = registro[d]
                self.tbwRegistros.setItem(fila, d, QTableWidgetItem(str(dato)))

            self.fnAlmacen()
        
        self.btnRegistrar.clicked.connect(self.Registro)
        self.btnRegistrar.clicked.connect(self.Cancelar)
        self.btnReporte.clicked.connect(self.Reporte)
        self.btnVolver.clicked.connect(self.fnVolver)

    def Registro(self):
        sucursal = self.cmbSucursal.currentIndex()
        t_movimiento = 1 if self.rdbEntrada.ischecked() else 0
        producto = self.txtProducto.text()
        cant = self.spbCantidad.value()
        cantidad = cant if t_movimiento == 1 else (cant * -1)

        valores = (t_movimiento, sucursal, producto, cantidad)
        con = conexion()
        c = con.cursor()
        sql = '''
            INSERT INTO almacen(tipo, sucursal, producto, cantidad)
            VALUES(%s, %s, %s, %s)
        '''
        c.execute(sql, valores)
        con.commit()

        if c.rowcount > 0:
            fila = self.tbwRegistros.rowCount()
            self.tbwRegistros.insertRow(fila)
            for d in range(len(valores)):
                dato = valores[d]
                self.tbwRegistros.setItem(fila, d, QTableWidgetItem(str(dato)))
            self.fnAlmacen()
        
        self.cmbSucursal.setCurrentIndex(-1)
        self.txtProducto.clear()
        self.spbCantidad.setValue(0)

    def Cancelar(self):
        self.cmbSucursal.setCurrentIndex(-1)
        self.txtProducto.clear()
        self.spbCantidad.setValue(0)

    def Reporte(self):
        con = conexion()
        suc = fnCarga(con, 'sucursal')
        sucursales = []
        for sucursal in suc:
            sucursales.append(sucursal[1])

        almacen_1 = self.sql(1000)
        almacen_2 = self.sql(2000)
        almacen_3 = self.sql(3000)
        almacen_4 = self.sql(4000)
        almacen_5 = self.sql(5000)

        y = np.array([almacen_1[0][1], almacen_2[0][1], almacen_3[0][1], almacen_4[0][1], almacen_5[0][1]])
        plt.pie(y, labels = sucursales)
        plt.legend(title = 'Sucursales')
        plt.show()
        
    
    def sql(self, almacen):
        con = conexion()
        c = con.cursor()
        s_sql = f'''
            SELECT a.sucursal, SUM(a.cantidad * p.costo)
            FROM productos AS p
            INNER JOIN almacen AS a
            WHERE a.sucursal = {almacen}
        '''
        c.execute(s_sql)
        recuento = c.fetchall()
        return recuento
    

    def fnAlmacen(self):
        for registro in range(self.tbwRegistros.rowCount()):
            if int(self.tbwRegistros.item(registro, 2).text()) == 1000:
                for celda in range(self.tbwRegistros.columnCount()):
                    self.tbwRegistros.item(registro, celda).setBackground(QtGui.QColor(204, 232, 226))
            elif int(self.tbwRegistros.item(registro, 2).text()) == 2000:
                for celda in range(self.tbwRegistros.columnCount()):
                    self.tbwRegistros.item(registro, celda).setBackground(QtGui.QColor(186, 202, 224))
            elif int(self.tbwRegistros.item(registro, 2).text()) == 3000:
                for celda in range(self.tbwRegistros.columnCount()):
                    self.tbwRegistros.item(registro, celda).setBackground(QtGui.QColor(202, 186, 224))
            elif int(self.tbwRegistros.item(registro, 2).text()) == 4000:
                for celda in range(self.tbwRegistros.columnCount()):
                    self.tbwRegistros.item(registro, celda).setBackground(QtGui.QColor(224, 186, 201))
            elif int(self.tbwRegistros.item(registro, 2).text()) == 5000:
                for celda in range(self.tbwRegistros.columnCount()):
                    self.tbwRegistros.item(registro, celda).setBackground(QtGui.QColor(224, 202, 186))
    
    def fnVolver(self):
        self.parent().show()
        self.close()
    

# ===========================
# =        Submódulos       =
# ===========================
class RegistroE(QMainWindow):
    def __init__(self, parent = None):
        super(RegistroE, self).__init__(parent)
        uic.loadUi(r'UI/Ui_RegEmpleado.ui', self)
        self.UiRegistro()

    def UiRegistro(self):
        self.btnRegistrarE.clicked.connect(self.fnRegistroE)
        self.btnCancelarE.clicked.connect(self.fnCancelar)
        
    def fnData(self):
        dia  = self.dateEmpleado.date().day()
        mes  = self.dateEmpleado.date().month()
        anio = self.dateEmpleado.date().year()

        nombre   = self.txtNombreE.text()
        apellido = self.txtApellidoE.text()
        nickname = self.txtNickname.text()
        contra   = self.txtPassword.text()
        puesto   = self.cmbPuesto.currentIndex() + 1
        correo   = self.txtCorreoE.text()
        telefono = self.txtTelefonoE.text()

        data = [nombre, apellido, [anio, mes, dia], nickname, contra, puesto, correo, telefono]
        return data
    
    def idEmpleado(self):
        datos    = self.fnData()
        nombre   = datos[0]
        apellido = datos[1]
        d_nac    = int(datos[2][2])
        m_nac    = int(datos[2][1])
        idEmp    = f'{nombre[:2]}{apellido[:2]}{"0" + str(d_nac) if datos[2][2] < 10 else d_nac}{"0" + str(m_nac) if datos[2][1] < 10 else m_nac}00'
        return idEmp.upper()

    def fnRegistroE(self):
        try:
            data  = self.fnData()
            idE   = self.idEmpleado()
            f_nac = f'{data[4][0]}-{data[4][1]}-{data[4][2]}'
            
            valores = (idE, data[0], data[1], f_nac, data[3], data[4], int(data[5]), data[6], data[7])

            con   = conexion()
            c     = con.cursor()
            sql = '''
                INSERT INTO empleados (id_empleado, nombre, apellido, fec_nacimiento,  nickname, contrasenia, puesto, correo, telefono)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            c.execute(sql, valores)
            con.commit()
        except:
            self.lblEstado.setText('Ha ocurrido un error')
        else:
            self.lblEstado.setText('Empleado registrado correctamente ✓')
        
        self.parent().show()
        self.close()
    
    def fnCancelar(self):
        self.parent().show()
        self.close()


class RegistroC(QMainWindow):
    def __init__(self, parent = None):
        super(RegistroC, self).__init__(parent)
        uic.loadUi(r'UI/Ui_RegCliente.ui', self)
        self.fnValidator()
        self.UiClientes()
    
    def fnValidator(self):
        self.txtCredito.setValidator(QDoubleValidator(0.99, 99.99, 2))
    
    def UiClientes(self):
        self.btnRegistrarC.clicked.connect(self.fnRegistrar)
        self.btnCancelarC.clicked.connect(self.fnCancelar)

    def fnRegistrar(self):
        nombre = self.txtNombreC.text()
        apellido = self.txtApellidoC.text()
        direccion = self.txtDireccionC.text()
        correo = self.txtCorreoC.text()
        estado = self.cmbEstadoC.currentIndex()
        credito = self.txtCredito.text()
        
        valores = (nombre, apellido, direccion, correo, estado, credito, credito)
        
        con = conexion()
        c = con.cursor()
        sql = '''
            INSERT INTO clientes (nombre, apellido, direccion, correo, estado, credito, saldo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        c.execute(sql, valores)
        con.commit()

        self.parent().show()
        self.close()

    def fnCancelar(self):
        self.parent().show()
        self.close()


        
# ==================================
# =        Funciones Globales      =
# ==================================
def conexion():
    con = mysql.connector.connect(
        host     = 'localhost',
        user     = 'root',
        password = 'admin',
        database = 'topes_gama'
    )
    return con

def fnCarga(conexion, tabla):
    con = conexion
    c   = con.cursor()
    sql = f'SELECT * FROM {tabla};'
    c.execute(sql)
    data = c.fetchall()
    return data

app = QApplication(sys.argv)
UIWindow = Login()
UIWindow.show()
sys.exit(app.exec_())