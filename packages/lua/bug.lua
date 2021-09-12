function incd (n)
    local s = string.format("%d", n)
    s = string.gsub(s, "%d$", function (d)
          assert(d ~= '9')
          return string.char(string.byte(d) + 1)
        end)
    return s
end

maxint = math.maxinteger

print(maxint)
print(incd(maxint))
a = (tonumber(incd(maxint)))
b = (maxint + 1.0)

print(string.format("%.0f", a))
print(string.format("%.0f", b))

print(string.format("%.f", maxint + .0))
