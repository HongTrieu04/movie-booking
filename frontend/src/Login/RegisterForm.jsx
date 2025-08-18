import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Form, Input, message } from "antd";

function RegisterForm() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleRegister = async (values) => {
    setLoading(true);
    try {
      const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: values.name,
          email: values.email,
          phone: values.phone,
          password: values.password
        }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Đăng ký thất bại");
      }

      await response.json();
      setSuccess(true);
      message.success("Đăng ký thành công! Bạn có thể đăng nhập ngay.");
    } catch (err) {
      message.error(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: 400,
        margin: "50px auto",
        padding: 20,
        border: "1px solid #f0f0f0",
        borderRadius: 8,
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)"
      }}
    >
      <h2 style={{ textAlign: "center", marginBottom: 24 }}>Đăng ký tài khoản</h2>

      <Form layout="vertical" onFinish={handleRegister} autoComplete="off">
        <Form.Item
          label="Họ tên"
          name="name"
          rules={[{ required: true, message: "Vui lòng nhập họ tên!" }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Email"
          name="email"
          rules={[
            { required: true, message: "Vui lòng nhập email!" },
            { type: "email", message: "Email không hợp lệ!" }
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Số điện thoại"
          name="phone"
          rules={[
            { pattern: /^[0-9]*$/, message: "Số điện thoại chỉ chứa số!" }
          ]}
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

        {/* Confirm Password */}
        <Form.Item
          label="Xác nhận mật khẩu"
          name="confirmPassword"
          dependencies={['password']}
          hasFeedback
          rules={[
            { required: true, message: "Vui lòng nhập lại mật khẩu!" },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue('password') === value) {
                  return Promise.resolve();
                }
                return Promise.reject(new Error('Mật khẩu không khớp!'));
              },
            }),
          ]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" block loading={loading}>
            Đăng ký
          </Button>
        </Form.Item>
      </Form>

      {success && (
        <Button type="default" block onClick={() => navigate("/login")}>
          Đăng nhập ngay
        </Button>
      )}
    </div>
  );
}

export default RegisterForm;
