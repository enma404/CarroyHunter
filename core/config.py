# core/config.py
# CarrotHunter - Configuration Manager
# Handle loading, saving, and managing configuration

import os
import json
import copy


# =============================================
# DEFAULT CONFIGURATION
# =============================================

DEFAULT_CONFIG = {
    "name": "CarrotHunter",
    "version": "1.0.0",
    "description": "Academic Security Research Tool - Isolated Lab Only",

    "scan_settings": {
        "timeout": 10,
        "threads": 10,
        "user_agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "max_redirects": 5,
        "verify_ssl": False,
        "follow_redirects": True,
        "retry_count": 2,
        "retry_delay": 1,
        "delay_between_requests": 0.1,
        "max_scan_time": 600
    },

    "modules": {
        "recon": {"enabled": True},
        "port": {"enabled": True},
        "web": {"enabled": True},
        "cms": {"enabled": True},
        "sqli": {"enabled": True, "severity": "CRITICAL", "time_based_delay": 5},
        "xss": {"enabled": True, "severity": "MEDIUM"},
        "lfi": {"enabled": True, "severity": "HIGH"},
        "cmdi": {"enabled": True, "severity": "CRITICAL", "time_based_delay": 5},
        "ssrf": {"enabled": True, "severity": "HIGH"},
        "upload": {"enabled": True, "severity": "CRITICAL"}
    },

    "cms_scanners": {
        "wordpress": {
            "enabled": True,
            "enumerate_users": True,
            "enumerate_plugins": True,
            "enumerate_themes": True,
            "check_xmlrpc": True,
            "check_rest_api": True
        },
        "joomla": {
            "enabled": True,
            "enumerate_components": True,
            "enumerate_templates": True,
            "check_config_exposure": True
        },
        "craft": {
            "enabled": True,
            "enumerate_plugins": True,
            "check_env_exposure": True,
            "check_graphql": True
        }
    },

    "exploitation": {
        "enabled": False,
        "require_confirmation": True,
        "isolated_lab_only": True,
        "save_loot": True,
        "loot_dir": "reports/loot",
        "max_exploit_attempts": 3
    },

    "output": {
        "report_dir": "reports",
        "log_dir": "logs",
        "save_json": True,
        "save_html": True,
        "save_log": True,
        "verbose": True,
        "color_output": True,
        "show_progress": True
    },

    "payloads": {
        "payload_dir": "payloads",
        "use_custom_payloads": True,
        "max_payloads_per_param": 100,
        "waf_bypass": False
    },

    "stealth": {
        "randomize_user_agents": False,
        "randomize_delays": True,
        "min_delay": 0.1,
        "max_delay": 0.5,
        "use_proxies": False,
        "proxy_list": []
    },

    "wordlists": {
        "wordlist_dir": "wordlists",
        "directories": "common_dirs.txt",
        "files": "common_files.txt",
        "parameters": "common_params.txt",
        "passwords": "common_passwords.txt"
    },

    "notifications": {
        "enabled": False,
        "webhook_url": "",
        "email": "",
        "slack_webhook": ""
    },

    "ethical_guardrails": {
        "require_authorization": True,
        "target_whitelist": [
            "127.0.0.1",
            "localhost",
            "testphp.vulnweb.com",
            "demo.testfire.net",
            "testhtml5.vulnweb.com"
        ],
        "block_public_targets": True,
        "warn_on_exploitation": True,
        "max_scan_intensity": "medium"
    }
}


# =============================================
# CONFIG CLASS
# =============================================

class Config:
    """Configuration manager"""

    def __init__(self, config_path=None, auto_load=True):
        """
        Initialize config

        Args:
            config_path: Path to config file
            auto_load: Load config on init
        """
        # Determine paths
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if config_path:
            self.config_path = config_path
        else:
            self.config_path = os.path.join(self.base_dir, "config", "config.json")

        # Set default config
        self.data = copy.deepcopy(DEFAULT_CONFIG)

        # Auto-load if file exists
        if auto_load and os.path.exists(self.config_path):
            self.load()

    # =============================================
    # LOAD / SAVE
    # =============================================

    def load(self):
        """Load configuration from file"""
        try:
            if not os.path.exists(self.config_path):
                self.save()  # Create default
                return True

            with open(self.config_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)

            # Merge with defaults (to add missing keys)
            self.data = self._merge_config(DEFAULT_CONFIG, loaded)
            return True

        except json.JSONDecodeError as e:
            print(f"[!] Config JSON error: {e}")
            print(f"[*] Using default config")
            self.data = copy.deepcopy(DEFAULT_CONFIG)
            return False

        except Exception as e:
            print(f"[!] Failed to load config: {e}")
            return False

    def save(self):
        """Save configuration to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"[!] Failed to save config: {e}")
            return False

    def reload(self):
        """Reload configuration"""
        return self.load()

    def reset(self):
        """Reset to default configuration"""
        self.data = copy.deepcopy(DEFAULT_CONFIG)
        return self.save()

    def _merge_config(self, default, loaded):
        """Merge loaded config with defaults (recursive)"""
        result = copy.deepcopy(default)

        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value

        return result

    # =============================================
    # GET VALUES
    # =============================================

    def get(self, key, default=None):
        """
        Get config value using dot notation

        Examples:
            config.get("scan_settings.timeout")
            config.get("modules.sqli.enabled")
        """
        if '.' in key:
            parts = key.split('.')
            value = self.data
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    return default
            return value

        return self.data.get(key, default)

    def get_section(self, section):
        """Get entire section"""
        return self.data.get(section, {})

    def get_scan_settings(self):
        """Get scan settings"""
        return self.data.get("scan_settings", {})

    def get_module_config(self, module):
        """Get module configuration"""
        return self.data.get("modules", {}).get(module, {})

    def is_module_enabled(self, module):
        """Check if module is enabled"""
        return self.get_module_config(module).get("enabled", True)

    # =============================================
    # SET VALUES
    # =============================================

    def set(self, key, value):
        """
        Set config value using dot notation

        Examples:
            config.set("scan_settings.timeout", 20)
            config.set("modules.sqli.enabled", False)
        """
        if '.' in key:
            parts = key.split('.')
            target = self.data

            for part in parts[:-1]:
                if part not in target:
                    target[part] = {}
                target = target[part]

            target[parts[-1]] = value
        else:
            self.data[key] = value

        return True

    def update(self, updates):
        """Bulk update config"""
        for key, value in updates.items():
            self.set(key, value)
        return True

    # =============================================
    # UTILITIES
    # =============================================

    def to_dict(self):
        """Return config as dictionary"""
        return copy.deepcopy(self.data)

    def to_json(self, indent=4):
        """Return config as JSON string"""
        return json.dumps(self.data, indent=indent, ensure_ascii=False)

    def exists(self):
        """Check if config file exists"""
        return os.path.exists(self.config_path)

    def get_path(self):
        """Get config file path"""
        return self.config_path

    # =============================================
    # CONVENIENCE PROPERTIES
    # =============================================

    @property
    def timeout(self):
        return self.get("scan_settings.timeout", 10)

    @property
    def threads(self):
        return self.get("scan_settings.threads", 10)

    @property
    def user_agent(self):
        return self.get("scan_settings.user_agent", "Mozilla/5.0")

    @property
    def verify_ssl(self):
        return self.get("scan_settings.verify_ssl", False)

    @property
    def follow_redirects(self):
        return self.get("scan_settings.follow_redirects", True)

    @property
    def report_dir(self):
        return self.get("output.report_dir", "reports")

    @property
    def log_dir(self):
        return self.get("output.log_dir", "logs")

    @property
    def verbose(self):
        return self.get("output.verbose", True)

    @property
    def payload_dir(self):
        return self.get("payloads.payload_dir", "payloads")

    @property
    def wordlist_dir(self):
        return self.get("wordlists.wordlist_dir", "wordlists")

    # =============================================
    # ABSOLUTE PATHS
    # =============================================

    def get_abs_path(self, relative_path):
        """Convert relative path to absolute"""
        if os.path.isabs(relative_path):
            return relative_path
        return os.path.join(self.base_dir, relative_path)

    def get_report_path(self):
        """Get absolute report directory path"""
        return self.get_abs_path(self.report_dir)

    def get_log_path(self):
        """Get absolute log directory path"""
        return self.get_abs_path(self.log_dir)

    def get_payload_path(self):
        """Get absolute payload directory path"""
        return self.get_abs_path(self.payload_dir)

    def get_wordlist_path(self):
        """Get absolute wordlist directory path"""
        return self.get_abs_path(self.wordlist_dir)

    # =============================================
    # DIRECTORY MANAGEMENT
    # =============================================

    def ensure_directories(self):
        """Ensure all required directories exist"""
        dirs = [
            self.get_report_path(),
            os.path.join(self.get_report_path(), "loot"),
            self.get_log_path(),
            self.get_payload_path(),
            os.path.join(self.get_payload_path(), "output"),
            self.get_wordlist_path(),
        ]

        for directory in dirs:
            os.makedirs(directory, exist_ok=True)

        return True

    # =============================================
    # DISPLAY
    # =============================================

    def show(self):
        """Print configuration (pretty)"""
        print(self.to_json())

    def summary(self):
        """Print config summary"""
        print(f"""
Configuration Summary
─────────────────────────────────────────
  Config Path:     {self.config_path}
  Timeout:         {self.timeout}s
  Threads:         {self.threads}
  User Agent:      {self.user_agent[:50]}...
  SSL Verify:      {self.verify_ssl}
  Report Dir:      {self.report_dir}
  Log Dir:         {self.log_dir}
  Payload Dir:     {self.payload_dir}
─────────────────────────────────────────
  Enabled Modules:
""")

        for module, settings in self.data.get("modules", {}).items():
            status = "✓" if settings.get("enabled", True) else "✗"
            print(f"    [{status}] {module}")


# =============================================
# GLOBAL CONFIG INSTANCE
# =============================================

_global_config = None


def get_config(config_path=None, reload=False):
    """
    Get global config instance

    Args:
        config_path: Custom config path (optional)
        reload: Force reload from disk

    Returns:
        Config instance
    """
    global _global_config

    if _global_config is None or reload:
        _global_config = Config(config_path)

    return _global_config


def load_config(config_path=None):
    """Load config (alias)"""
    return get_config(config_path, reload=True)


def save_config(config=None):
    """Save config"""
    if config is None:
        config = get_config()
    return config.save()


def reset_config():
    """Reset config to defaults"""
    config = get_config()
    return config.reset()


# =============================================
# EXPORTS
# =============================================

__all__ = [
    "Config",
    "DEFAULT_CONFIG",
    "get_config",
    "load_config",
    "save_config",
    "reset_config",
]