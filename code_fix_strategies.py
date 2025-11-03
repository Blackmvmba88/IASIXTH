"""
🔧 ESTRATEGIAS DE FIXES DE CÓDIGO
Módulo de funciones de reparación automática de código
"""
import re
from config import LINE_LENGTH_LIMIT


def fix_unused_imports(file_path, unused_imports):
    """Remover imports no usados"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        filtered_lines = []
        for i, line in enumerate(lines, 1):
            should_remove = False
            for unused_name, line_num in unused_imports.items():
                if i == line_num and unused_name in line:
                    should_remove = True
                    break

            if not should_remove:
                filtered_lines.append(line)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(filtered_lines)

        return True
    except Exception:
        return False


def smart_line_break(line):
    """Romper líneas largas de manera inteligente"""
    if len(line) <= LINE_LENGTH_LIMIT:
        return line

    # Si tiene paréntesis, romper ahí
    if '(' in line and ')' in line:
        parts = line.split('(', 1)
        if len(parts) > 1:
            return parts[0] + '(\n        ' + parts[1]

    # Si tiene comas, romper ahí
    if ',' in line:
        parts = line.split(',', 1)
        return parts[0] + ',\n        ' + parts[1]

    # Si es muy larga, cortar con continuación
    if len(line) > LINE_LENGTH_LIMIT:
        split_point = LINE_LENGTH_LIMIT - 4
        return line[:split_point] + ' \\\n    ' + line[split_point:]

    return line


def fix_long_lines(file_path, long_lines_info):
    """Acortar líneas largas inteligentemente"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            if len(line) > LINE_LENGTH_LIMIT:
                fixed_line = smart_line_break(line)
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(fixed_lines))

        return True
    except Exception:
        return False


def fix_whitespace(file_path, whitespace_issues):
    """Limpiar espacios en blanco"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Limpiar trailing whitespace
        lines = content.split('\n')
        clean_lines = [line.rstrip() for line in lines]

        # Asegurar newline al final
        if clean_lines and clean_lines[-1] != '':
            clean_lines.append('')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(clean_lines))

        return True
    except Exception:
        return False


def fix_syntax_errors(file_path, syntax_error_info):
    """Arreglar errores de sintaxis básicos"""
    # TODO: Implementar fixes comunes de sintaxis
    # Por ahora retornar False para indicar que no está implementado
    return False


def fix_dependencies(file_path, dependency_issues):
    """Resolver conflictos de dependencias"""
    # TODO: Implementar resolución inteligente de dependencias
    # Por ahora retornar False para indicar que no está implementado
    return False


def optimize_performance(file_path, performance_issues):
    """Optimizar rendimiento automáticamente"""
    # TODO: Implementar optimizaciones automáticas
    # Por ahora retornar False para indicar que no está implementado
    return False
