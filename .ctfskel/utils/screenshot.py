import os
import hashlib
from urllib.parse import urlparse, quote
from datetime import datetime
from selenium.webdriver.firefox.options import Options
from seleniumrequests import Firefox
from IPython.display import display, Image

def screenshot(
    session,
    url,
    savelocation=None,
    width=1440,
    height=900,
    headless=True,
    zoom=0.5,
    element_selector=None
):
    """
    Screenshot a URL using seleniumrequests.Firefox with proxy 
    config auto-detected from the requests.Session.
    """
    # Filename logic
    parsed = urlparse(url)
    domain = parsed.hostname or "site"
    path = parsed.path or ""
    path_part = quote(path.strip("/").replace("/", "_")) if path.strip("/") else "root"
    query_part = quote(parsed.query) if parsed.query else ""
    uri_part = f"{path_part}"
    if query_part:
        uri_part += f"_{query_part}"
    timestamp = datetime.now().strftime("%m-%d-%H-%M")
    selector_part = ""
    if element_selector:
        selector_part = element_selector.replace("#", "id_").replace(".", "class_").replace(" ", "_")
    session_id = str(session.cookies.get_dict())+uri_part
    sha1 = hashlib.sha1(session_id.encode()).hexdigest()[:6]
    if not savelocation:
        os.makedirs("engagement_files", exist_ok=True)
        filename = f"{domain}_{timestamp}_{sha1}"
        if selector_part:
            filename += f"_{selector_part}"
        filename += ".png"
        savelocation = os.path.join("engagement_files", filename)

    # --- Detect proxy from session, prefer SOCKS, fallback to HTTP ---
    proxy_type = None
    proxy_host = None
    proxy_port = None
    proxy_dns = False
    if hasattr(session, "proxies") and session.proxies:
        # Prefer any value that has a socks* scheme in the URL (not just the key!)
        for key, proxy_url in session.proxies.items():
            if not proxy_url:
                continue
            parsed_proxy = urlparse(proxy_url)
            scheme = parsed_proxy.scheme.lower()
            if scheme.startswith("socks"):
                proxy_type = scheme
                proxy_host = parsed_proxy.hostname
                proxy_port = parsed_proxy.port
                if scheme.endswith("h"):
                    proxy_dns = True
                break
        # If no SOCKS, fallback to http/https (again, parse the scheme)
        if not proxy_type:
            for key, proxy_url in session.proxies.items():
                if not proxy_url:
                    continue
                parsed_proxy = urlparse(proxy_url)
                scheme = parsed_proxy.scheme.lower()
                if scheme.startswith("http"):
                    proxy_type = scheme
                    proxy_host = parsed_proxy.hostname
                    proxy_port = parsed_proxy.port
                    break

    # ---- Set up Firefox options ----
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument(f"--width={width}")
    options.add_argument(f"--height={height}")

    # Set proxy preferences as per Selenium 4
    if proxy_type and proxy_host and proxy_port:
        options.set_preference('network.proxy.type', 1)
        options.set_preference('network.proxy.no_proxies_on', '')  # CRUCIAL: no proxy bypass, even for localhost!
        options.set_preference('network.proxy.allow_hijacking_localhost', True)
        if proxy_type.startswith("socks"):
            options.set_preference('network.proxy.socks', proxy_host)
            options.set_preference('network.proxy.socks_port', proxy_port)
            options.set_preference('network.proxy.socks_version', 5)
            options.set_preference('network.proxy.socks_remote_dns', proxy_dns)
            # Clear HTTP/SSL proxy
            options.set_preference('network.proxy.http', "")
            options.set_preference('network.proxy.http_port', 0)
            options.set_preference('network.proxy.ssl', "")
            options.set_preference('network.proxy.ssl_port', 0)
        elif proxy_type.startswith("http"):
            options.set_preference('network.proxy.http', proxy_host)
            options.set_preference('network.proxy.http_port', proxy_port)
            options.set_preference('network.proxy.ssl', proxy_host)
            options.set_preference('network.proxy.ssl_port', proxy_port)
            options.set_preference('network.proxy.socks', "")
            options.set_preference('network.proxy.socks_port', 0)

    driver = Firefox(options=options)
    driver.set_window_size(width, height)

    driver.get(url)  # Needed to set the domain context

    # Add all cookies from the requests session that match the target domain
    for c in session.cookies:
        # Only set cookies for the current domain (or superdomain)
        cookie_domain = c.domain if hasattr(c, "domain") else parsed.hostname
        if parsed.hostname.endswith(cookie_domain.lstrip('.')):
            cookie_dict = {
                'name': c.name,
                'value': c.value,
                'path': getattr(c, 'path', '/'),
                # domain is optional in selenium; only set if cross-domain
            }
            # Only set domain if it's a superdomain cookie
            if cookie_domain != parsed.hostname:
                cookie_dict['domain'] = cookie_domain
            try:
                driver.add_cookie(cookie_dict)
            except Exception as e:
                print(f"Failed to add cookie {c.name}: {e}")

    driver.refresh()

    headers = dict(session.headers) if hasattr(session, "headers") else {}
    
    driver.request('GET', url, headers=headers)

    # Set the zoom using JS
    try:
        driver.execute_script(f"document.body.style.zoom='{zoom * 100}%'")
    except Exception:
        pass

    # Screenshot logic
    if element_selector:
        try:
            element = driver.find_element("css selector", element_selector)
            element.screenshot(savelocation)
        except Exception as e:
            print(f"Could not find element by selector '{element_selector}': {e}")
            driver.save_screenshot(savelocation)
    else:
        driver.save_screenshot(savelocation)

    driver.quit()
    display(Image(filename=savelocation))
    return savelocation
