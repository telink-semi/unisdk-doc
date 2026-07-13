/**
 * UniSDK Version Switcher
 *
 * Reads versions.json from the root of the deployed site and populates
 * a version selector dropdown. When the user selects a different version,
 * redirects to the corresponding URL.
 *
 * versions.json format:
 * {
 *   "versions": [
 *     {"name": "main", "url": "/en/main/", "label": "latest"},
 *     {"name": "v0.2.0", "url": "/en/v0.2.0/", "label": "v0.2.0"}
 *   ]
 * }
 */

(function() {
  'use strict';

  var CURRENT_VERSION = typeof currentVersion !== 'undefined' ? currentVersion : 'main';
  var CURRENT_LANG = typeof currentLang !== 'undefined' ? currentLang : 'en';

  function getBaseUrl() {
    // Determine the root URL of the deployment
    var scripts = document.getElementsByTagName('script');
    var currentScript = scripts[scripts.length - 1];
    var scriptSrc = currentScript.src;
    // Remove the script path to get the site root
    var root = scriptSrc.substring(0, scriptSrc.lastIndexOf('/_static/'));
    return root;
  }

  function initVersionSelector() {
    var select = document.getElementById('version-select');
    if (!select) return;

    // Determine the base URL for fetching versions.json
    // Walk up from the current page URL to find the root
    var pathParts = window.location.pathname.split('/').filter(Boolean);
    // The root is at the first level (e.g., /en/main/ -> root is /)
    var versionsUrl = '/versions.json';

    fetch(versionsUrl)
      .then(function(response) {
        if (!response.ok) throw new Error('Failed to load versions.json');
        return response.json();
      })
      .then(function(data) {
        // Clear loading option
        select.innerHTML = '';

        if (!data.versions || data.versions.length === 0) {
          select.innerHTML = '<option value="">No versions</option>';
          return;
        }

        // Group versions by language
        var enVersions = data.versions.filter(function(v) { return v.lang === 'en'; });
        var zhVersions = data.versions.filter(function(v) { return v.lang === 'zh'; });

        var currentLangVersions = CURRENT_LANG === 'zh' ? zhVersions : enVersions;
        if (currentLangVersions.length === 0) {
          currentLangVersions = data.versions;
        }

        // Add optgroup for current language
        if (currentLangVersions.length > 0) {
          var label = CURRENT_LANG === 'zh' ? '中文版' : 'English';
          var group = document.createElement('optgroup');
          group.label = label;

          currentLangVersions.forEach(function(v) {
            var opt = document.createElement('option');
            opt.value = v.url;
            opt.textContent = v.label;
            if (v.name === CURRENT_VERSION) {
              opt.selected = true;
            }
            group.appendChild(opt);
          });

          select.appendChild(group);
        }

        // If no versions match, show all
        if (select.options.length === 0) {
          data.versions.forEach(function(v) {
            var opt = document.createElement('option');
            opt.value = v.url;
            opt.textContent = v.label;
            select.appendChild(opt);
          });
        }
      })
      .catch(function(err) {
        console.warn('Version switcher: unable to load versions.json', err);
        select.innerHTML = '<option value="">' + CURRENT_VERSION + '</option>';
      });
  }

  window.switchVersion = function(url) {
    if (url) {
      window.location.href = url;
    }
  };

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initVersionSelector);
  } else {
    initVersionSelector();
  }
})();