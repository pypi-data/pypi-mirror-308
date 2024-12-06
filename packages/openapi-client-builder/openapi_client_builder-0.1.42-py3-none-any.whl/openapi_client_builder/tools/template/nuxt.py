# template
temp_header = """
export function getCookie(cname: string) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

export async function api(url: string, options: RequestInit | undefined) {
  const BasisApiURL = "http://localhost:8000"
  try {
      const res = await fetch(`${BasisApiURL}${url}`, options)
      const data = await res.json()
      return data
  } catch (error) {
      return {
          "error": "An error occurred.",
          "code": 500,
          "message": "Server Error."
      }
  }
}

export async function apiFile(url: string, options: RequestInit | undefined) {
  const BasisApiURL = "http://localhost:8000"
  try {
      const res = await fetch(`${BasisApiURL}/api/${url}`, options)
      const blob = await res.blob();
      return blob;
  } catch (error) {
      return {
          "error": "An error occurred.",
          "code": 500,
          "message": "Server Error."
      }
  }
}

export function getHeaders() {
    return {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${getCookie("token")}`,
    };
}
"""

temp_schemas = """
type %s = {
%s
}
"""

temp_api = """
export async function %s {
  const url = %s;
  const options = {
    method: "%s",
    headers: getHeaders(),%s
  };
  return await %s(url, options);
}
"""
