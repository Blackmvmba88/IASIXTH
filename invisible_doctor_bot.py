"""
🤖 DOCTOR BOT INVISIBLE - ARREGLADOR AUTOMÁTICO 🕵️‍♂️
Iyari Cancino Gomez & Copilot - Inteligencia Oculta

El bot que arregla problemas sin que nadie vea venir esta manera de pensar
"""
import os
import ast
import time
import threading
from datetime import datetime
import json
import sqlite3
from contextlib import contextmanager
from config import LINE_LENGTH_LIMIT, MONITORING_INTERVAL
from code_fix_strategies import (
    fix_unused_imports, fix_long_lines, fix_whitespace,
    fix_syntax_errors, fix_dependencies, optimize_performance
)


class InvisibleDoctorBot:
    """Bot invisible que arregla todo automáticamente"""

    def __init__(self, project_path="."):
        self.project_path = project_path
        self.healing_db = "doctor_bot_intelligence.db"
        self.learning_patterns = {}
        self.is_monitoring = False
        self.monitor_thread = None

        # Patrones de inteligencia oculta
        self.smart_fixes = {
            'imports_unused': self._wrap_fix(fix_unused_imports),
            'lines_too_long': self._wrap_fix(fix_long_lines),
            'whitespace_issues': self._wrap_fix(fix_whitespace),
            'syntax_errors': self._wrap_fix(fix_syntax_errors),
            'dependency_conflicts': self._wrap_fix(fix_dependencies),
            'performance_issues': self._wrap_fix(optimize_performance)
        }

        self.init_intelligence_database()
        print("🕵️‍♂️ Doctor Bot Invisible iniciado... Nadie sospecha nada.")

    def _wrap_fix(self, fix_func):
        """Envolver función de fix para manejar la firma del problema"""
        def wrapper(problem):
            return fix_func(problem['file'], problem['details'])
        return wrapper

    @contextmanager
    def _get_db_connection(self):
        """Context manager para conexiones de base de datos"""
        conn = sqlite3.connect(self.healing_db)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_intelligence_database(self):
        """Base de datos de inteligencia oculta"""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS healing_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT NOT NULL,
                    problem_type TEXT NOT NULL,
                    fix_applied TEXT NOT NULL,
                    success BOOLEAN,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS intelligence_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_name TEXT NOT NULL,
                    detection_rule TEXT NOT NULL,
                    fix_formula TEXT NOT NULL,
                    success_rate REAL DEFAULT 0.0,
                    times_used INTEGER DEFAULT 0
                )
            ''')

    def start_invisible_monitoring(self):
        """Iniciar monitoreo invisible del proyecto"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(
                target=self._invisible_watch_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            print("👁️ Vigilancia invisible activada... El proyecto está protegido.")

    def _invisible_watch_loop(self):
        """Bucle de vigilancia invisible"""
        while self.is_monitoring:
            try:
                # Escanear proyecto periódicamente
                problems = self._scan_for_problems()

                if problems:
                    print(
                        f"🔍 Detectados {len(problems)} problemas. "
                        "Aplicando fixes invisibles...")
                    self._apply_invisible_fixes(problems)

                time.sleep(MONITORING_INTERVAL)

            except Exception as e:
                self._log_intelligence(f"Error en monitoreo: {e}")
                time.sleep(5)

    def _scan_for_problems(self):
        """Escanear proyecto en busca de problemas"""
        problems = []

        # Buscar archivos Python
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    file_problems = self._analyze_file(file_path)
                    problems.extend(file_problems)

        return problems

    def _analyze_file(self, file_path):
        """Analizar archivo en busca de problemas específicos"""
        problems = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Detectar imports no usados
            unused_imports = self._detect_unused_imports(content)
            if unused_imports:
                problems.append({
                    'file': file_path,
                    'type': 'imports_unused',
                    'details': unused_imports
                })

            # Detectar líneas muy largas
            long_lines = self._detect_long_lines(lines)
            if long_lines:
                problems.append({
                    'file': file_path,
                    'type': 'lines_too_long',
                    'details': long_lines
                })

            # Detectar problemas de whitespace
            whitespace_issues = self._detect_whitespace_issues(lines)
            if whitespace_issues:
                problems.append({
                    'file': file_path,
                    'type': 'whitespace_issues',
                    'details': whitespace_issues
                })

        except Exception as e:
            self._log_intelligence(f"Error analizando {file_path}: {e}")

        return problems

    def _detect_unused_imports(self, content):
        """Detectar imports no usados con inteligencia avanzada"""
        try:
            tree = ast.parse(content)
            imports = {}
            used_names = set()

            # Recopilar imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports[alias.name] = node.lineno
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        imports[alias.name] = node.lineno

                # Recopilar nombres usados
                elif isinstance(node, ast.Name):
                    used_names.add(node.id)

            # Encontrar imports no usados
            unused = {}
            for name, line in imports.items():
                if name not in used_names:
                    unused[name] = line

            return unused

        except BaseException:
            return {}

    def _detect_long_lines(self, lines):
        """Detectar líneas demasiado largas"""
        long_lines = {}
        for i, line in enumerate(lines, 1):
            if len(line) > LINE_LENGTH_LIMIT:
                long_lines[i] = len(line)
        return long_lines

    def _detect_whitespace_issues(self, lines):
        """Detectar problemas de espacios en blanco"""
        issues = {}
        for i, line in enumerate(lines, 1):
            if line.endswith(' ') or line.endswith('\t'):
                issues[i] = "trailing_whitespace"
            elif line.strip() == '' and (line.count(' ') > 0 or line.count('\t') > 0):
                issues[i] = "whitespace_only_line"
        return issues

    def _apply_invisible_fixes(self, problems):
        """Aplicar fixes invisibles a los problemas detectados"""
        for problem in problems:
            try:
                fix_func = self.smart_fixes.get(problem['type'])
                if fix_func:
                    success = fix_func(problem)
                    self._log_fix(problem, success)

                    if success:
                        print(
                            f"✅ Fix invisible aplicado: {
                                problem['type']} en {
                                problem['file']}")

            except Exception as e:
                print(f"❌ Error aplicando fix: {e}")



    def _log_fix(self, problem, success):
        """Registrar fix aplicado en base de inteligencia"""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO healing_history (file_path, problem_type, fix_applied, success)
                VALUES (?, ?, ?, ?)
            ''', (problem['file'], problem['type'], str(problem['details']), success))

    def _log_intelligence(self, message):
        """Log de inteligencia oculta"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"🧠 [{timestamp}] {message}")

    def get_intelligence_report(self):
        """Obtener reporte de inteligencia del bot"""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                'SELECT COUNT(*) FROM healing_history WHERE success = 1')
            successful_fixes = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM healing_history')
            total_fixes = cursor.fetchone()[0]

        return {
            'total_fixes_applied': total_fixes,
            'successful_fixes': successful_fixes,
            'success_rate': (
                successful_fixes / total_fixes * 100
            ) if total_fixes > 0 else 0,
            'status': '🕵️‍♂️ Operando en las sombras',
            'intelligence_level': 'MÁXIMO'}

    def emergency_heal_project(self):
        """Sanación de emergencia de todo el proyecto"""
        print("🚨 SANACIÓN DE EMERGENCIA ACTIVADA 🚨")
        problems = self._scan_for_problems()

        if problems:
            print(f"🔧 Reparando {len(problems)} problemas críticos...")
            self._apply_invisible_fixes(problems)
            print("✅ Proyecto sanado completamente")
        else:
            print("💚 Proyecto en perfecto estado de salud")

        return self.get_intelligence_report()


if __name__ == "__main__":
    print("🤖 INICIANDO DOCTOR BOT INVISIBLE...")
    print("🕵️‍♂️ Preparando inteligencia oculta...")

    doctor = InvisibleDoctorBot()

    # Sanación inmediata
    report = doctor.emergency_heal_project()
    print(f"\n📊 REPORTE DE INTELIGENCIA:")
    print(f"   Fixes aplicados: {report['total_fixes_applied']}")
    print(f"   Éxito: {report['success_rate']:.1f}%")
    print(f"   Estado: {report['status']}")

    # Iniciar monitoreo invisible
    doctor.start_invisible_monitoring()

    print("\n🎵 El Doctor Bot Invisible está cuidando el proyecto...")
    print("💤 Durmiendo en las sombras, siempre vigilante...")

    try:
        while True:
            time.sleep(60)  # Dormir 1 minuto

    except KeyboardInterrupt:
        print("\n🕵️‍♂️ Doctor Bot regresando a las sombras...")
        doctor.is_monitoring = False
