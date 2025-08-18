import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Checkbox, Form, Input, Divider, message } from "antd";

function LoginForm() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  // --- Login DB ---
  const handleLogin = async (values) => {
    setLoading(true);
    try {
      const response = await fetch("/api/auth/login-db", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: values.email, password: values.password }),
      });

      if (!response.ok) throw new Error("Đăng nhập thất bại");

      const data = await response.json();
      localStorage.setItem("access_token", data.access_token);

      // Lấy thông tin user
      const meRes = await fetch("/api/auth/me", {
        headers: { Authorization: `Bearer ${data.access_token}` },
      });

      if (!meRes.ok) throw new Error("Không thể lấy thông tin người dùng");

      const meData = await meRes.json();
      console.log("User info:", meData);

      message.success("Đăng nhập thành công!");
      navigate("/");
    } catch (err) {
      message.error(err.message);
    } finally {
      setLoading(false);
    }
  };

  // --- Login Keycloak ---
  const handleKeycloakLogin = () => {
    const keycloakUrl =
      "http://localhost:8080/auth/realms/movie/protocol/openid-connect/auth";
    const clientId = "movie-frontend";
    const redirectUri = "http://localhost:3000/callback";
    const scope = "openid email profile";

    window.location.href = `${keycloakUrl}?client_id=${clientId}&redirect_uri=${encodeURIComponent(
      redirectUri
    )}&response_type=code&scope=${scope}`;
  };

  // --- Go to Register Page ---
  const handleGoRegister = () => {
    navigate("/register");
  };

  return (
    <div style={{ maxWidth: 400, margin: "50px auto", padding: 20, border: "1px solid #f0f0f0", borderRadius: 8, boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
      <h2 style={{ textAlign: "center", marginBottom: 24 }}>Đăng nhập</h2>

      <Form
        name="login"
        layout="vertical"
        onFinish={handleLogin}
        autoComplete="off"
      >
        <Form.Item
          label="Email"
          name="email"
          rules={[{ required: true, message: "Vui lòng nhập email!" }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Mật khẩu"
          name="password"
          rules={[{ required: true, message: "Vui lòng nhập mật khẩu!" }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item name="remember" valuePropName="checked">
          <Checkbox>Ghi nhớ đăng nhập</Checkbox>
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" block loading={loading}>
            Đăng nhập bằng Email
          </Button>
        </Form.Item>
      </Form>

      <Divider>Hoặc</Divider>

      <Button
        type="primary"
        block
        style={{ background: "#4c6ef5", borderColor: "#4c6ef5", marginBottom: 8 }}
        onClick={handleKeycloakLogin}
      >
        Đăng nhập với Keycloak
      </Button>

      <Button type="default" block style={{ background: "green", color: "white" }} onClick={handleGoRegister}>
        Đăng ký tài khoản
      </Button>
    </div>
  );
}

export default LoginForm;
