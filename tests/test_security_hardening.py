import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(relative):
    spec = importlib.util.spec_from_file_location('subject', ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AlgebraSecurityTests(unittest.TestCase):
    def setUp(self):
        base = 'skills/loki-mode/benchmarks/results/'
        self.functions = [load(base + folder + '/160.py').do_algebra for folder in
                          ('humaneval-loki-solutions', '2026-01-05-00-49-17/humaneval-solutions')]

    def test_preserves_precedence_associativity_and_floor_division(self):
        cases = [(['+', '*', '-'], [2, 3, 4, 5], 9),
                 (['**', '**'], [2, 3, 2], 512),
                 (['-', '//'], [1, 7, 2], -2),
                 (['//', '*'], [9, 2, 3], 12), ([], [5], 5)]
        for fn in self.functions:
            for operators, operands, expected in cases:
                self.assertEqual(fn(operators, operands), expected)

    def test_rejects_non_data_operators_and_operands(self):
        class NotAnInteger:
            def __str__(self):
                raise AssertionError('Must not coerce arbitrary objects')
        for fn in self.functions:
            for operators, operands in [(['+__import__("os").getcwd()+'], [1, 2]),
                                        (['+'], [NotAnInteger(), 2]),
                                        (['+'], ['1', 2]), (['+'], [True, 2]),
                                        (['+'], [1]), ([], []), (['/'], [2, 1])]:
                with self.assertRaises(ValueError):
                    fn(operators, operands)


class ProvisioningSecurityTests(unittest.TestCase):
    def setUp(self):
        self.module = load('skills/ms365-tenant-manager/scripts/user_management.py')

    def test_user_fields_are_powershell_literal_data(self):
        value = "O'Brien$(Write-Error PWNED)`\"; Stop-Process; #"
        quoted = self.module._ps_literal(value)
        self.assertEqual(quoted, "'" + value.replace("'", "''") + "'")
        script = self.module.UserLifecycleManager('example.invalid').generate_user_creation_script([
            dict(username='user', display_name=value, department=value, license_sku=value)])
        for field in ('DisplayName', 'Department', 'LicenseSku'):
            self.assertIn(field + ' = ' + quoted, script)

    def test_provisioning_uses_crypto_randomness_and_redacts_export(self):
        script = self.module.UserLifecycleManager('example.invalid').generate_user_creation_script([{}])
        self.assertIn('RandomNumberGenerator]::Create()', script)
        self.assertIn('New-Object byte[] 32', script)
        self.assertNotIn('Get-Random -Minimum', script)
        self.assertIn('Password = New-ProvisioningPassword', script)
        self.assertIn('Select-Object * -ExcludeProperty PasswordProfile | Export-Csv', script)

    def test_offboarding_keeps_email_and_domain_out_of_executable_syntax(self):
        hostile = '#>\n$(Write-Error PWNED)\n"@\n'
        script = self.module.UserLifecycleManager(hostile).generate_user_offboarding_script(hostile)
        self.assertIn('$userEmail = ' + self.module._ps_literal(hostile), script)
        self.assertIn('$supportEmail = ' + self.module._ps_literal('support@' + hostile), script)
        self.assertIn("$reportUser = $userEmail -replace '[^A-Za-z0-9_.@-]', '_'", script)
        self.assertNotIn('Securely offboards user: ' + hostile, script)


if __name__ == '__main__':
    unittest.main()
